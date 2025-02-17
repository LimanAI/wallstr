from datetime import timedelta
from typing import Annotated
from uuid import UUID

import boto3
import botocore.config
from fastapi import APIRouter, Depends, HTTPException, Request, status
from weaviate.classes.query import Filter

from wallstr.auth.dependencies import Auth
from wallstr.auth.schemas import HTTPUnauthorizedError
from wallstr.conf import settings
from wallstr.documents.models import DocumentStatus
from wallstr.documents.schemas import DocumentSection
from wallstr.documents.services import DocumentService
from wallstr.documents.tasks import process_document
from wallstr.models.base import utc_now
from wallstr.openapi import generate_unique_id_function

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    generate_unique_id_function=generate_unique_id_function(3),
    responses={401: {"model": HTTPUnauthorizedError}},
)


@router.put(
    "/{id}/mark-uploaded",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Mark document as uploaded",
)
async def mark_document_uploaded(
    auth: Auth,
    id: UUID,
    document_svc: Annotated[DocumentService, Depends(DocumentService.inject_svc)],
) -> None:
    await document_svc.mark_document_uploaded(auth.user_id, id)
    process_document.send(document_id=str(id))


@router.get("/section/{section_id}")
async def get_document_by_section(
    request: Request,
    auth: Auth,
    section_id: UUID,
    document_svc: Annotated[DocumentService, Depends(DocumentService.inject_svc)],
) -> DocumentSection:
    wvc = request.state.wvc

    collection = wvc.collections.get("Documents")
    response = await collection.query.fetch_objects(
        filters=(
            Filter.by_id().equal(section_id)
            & Filter.by_property("user_id").equal(auth.user_id)
        ),
        limit=1,
    )
    if not response.objects:
        raise HTTPException(status_code=404, detail="Section not found")

    chunk = response.objects[0]
    document = await document_svc.get_document(chunk.properties["document_id"])
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    s3_client = boto3.client(
        "s3",
        endpoint_url=str(settings.STORAGE_URL),
        aws_access_key_id=settings.STORAGE_ACCESS_KEY.get_secret_value(),
        aws_secret_access_key=settings.STORAGE_SECRET_KEY.get_secret_value(),
        config=botocore.config.Config(signature_version="s3v4"),
    )
    document_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.STORAGE_BUCKET,
            "Key": document.storage_path,
        },
        ExpiresIn=60 * 5,
    )

    section = DocumentSection(
        document_title=document.filename,
        document_url=document_url,
        page_number=chunk.properties["metadata"]["page_number"],
        bbox=(1, 1, 1, 1),
    )

    return section


@router.get(
    "/{document_id}/url",
    responses={
        404: {"description": "Document not found"},
        403: {"description": "Forbidden"},
    },
)
async def get_document_url(
    auth: Auth,
    document_id: UUID,
    document_svc: Annotated[DocumentService, Depends(DocumentService.inject_svc)],
) -> str:
    document = await document_svc.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.user_id != auth.user_id:
        raise HTTPException(
            status_code=403, detail="User is not the owner of the document"
        )

    s3_client = boto3.client(
        "s3",
        endpoint_url=str(settings.STORAGE_URL),
        aws_access_key_id=settings.STORAGE_ACCESS_KEY.get_secret_value(),
        aws_secret_access_key=settings.STORAGE_SECRET_KEY.get_secret_value(),
        config=botocore.config.Config(signature_version="s3v4"),
    )
    document_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.STORAGE_BUCKET,
            "Key": document.storage_path,
        },
        ExpiresIn=60 * 5,
    )
    return document_url


@router.post(
    "/{document_id}/process",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Trigger document processing manually",
    responses={
        404: {"description": "Document not found"},
        403: {"description": "Forbidden"},
    },
)
async def trigger_processing(
    auth: Auth,
    document_id: UUID,
    document_svc: Annotated[DocumentService, Depends(DocumentService.inject_svc)],
) -> None:
    document = await document_svc.get_document(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    if document.user_id != auth.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not the owner of the document",
        )
    if document.status == DocumentStatus.UPLOADING:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Document is not uploaded yet"
        )

    # TODO: move to the SQLAlchemy model field
    if (
        document.status == DocumentStatus.PROCESSING
        and document.error is None
        and document.updated_at
        and utc_now() - document.updated_at <= timedelta(minutes=10)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Document is already being processed",
        )

    process_document.send(document_id=str(document_id))
