from typing import cast
from uuid import UUID, uuid4

import structlog
from dramatiq.middleware import CurrentMessage
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from sqlalchemy import sql
from sqlalchemy.ext.asyncio import AsyncSession
from structlog.contextvars import bind_contextvars

from wallstr.chat.llm import SYSTEM_PROMPT
from wallstr.chat.memo.tasks import generate_memo
from wallstr.chat.models import ChatMessageModel, ChatMessageRole, ChatMessageType
from wallstr.chat.schemas import (
    ChatMessageEndSSE,
    ChatMessageSSE,
    ChatMessageStartSSE,
)
from wallstr.chat.services import ChatService
from wallstr.core.llm import SUPPORTED_LLM_MODELS_TYPES, get_llm
from wallstr.documents.llm import get_rag
from wallstr.documents.weaviate import get_weaviate_client
from wallstr.logging import debug
from wallstr.worker import dramatiq

logger = structlog.get_logger()


class Action(BaseModel):
    build_memo: bool = Field(description="User would to build a memo")


@dramatiq.actor  # type: ignore
async def process_chat_message(
    message_id: str, model: SUPPORTED_LLM_MODELS_TYPES = "gpt-4o"
) -> None:
    ctx = CurrentMessage.get_current_message()
    if not ctx:
        raise Exception("No ctx message")

    db_session = ctx.options.get("session")
    if not db_session:
        raise Exception("No session")

    chat_svc = ChatService(db_session)
    message = await chat_svc.get_chat_message(UUID(message_id))
    if not message:
        raise Exception("Message not found")

    if not message.content:
        # Not reply on an empty message
        return

    redis = ctx.options.get("redis")
    if not redis:
        raise Exception("No redis")

    bind_contextvars(chat_id=message.chat_id, message_id=message.id)
    llm = get_llm(model=model)

    response = await llm.with_structured_output(Action, strict=True).ainvoke(
        [
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(
                content="Define what users would like to do, building memo must be asked explicitly."
            ),
            HumanMessage(content=message.content),
        ]
    )
    action = cast(Action, response)

    if action.build_memo:
        new_message = await chat_svc.create_chat_message(
            chat_id=message.chat_id,
            message="",
            role=ChatMessageRole.ASSISTANT,
            message_type=ChatMessageType.MEMO,
        )
        logger.info(f"Generating memo for message {message.id}")
        generate_memo.send(str(new_message.id), message.content)
        return

    topic = f"{message.user_id}:{message.chat_id}:{message.id}"
    new_message_id = uuid4()
    await redis.publish(topic, ChatMessageStartSSE(id=new_message_id).model_dump_json())

    document_ids = await chat_svc.get_chat_document_ids(message.chat_id)
    logger.info(f"Found {len(document_ids)} documents for chat {message.chat_id}")
    llm_context = await get_llm_context(db_session, document_ids, message)
    chunks: list[str] = []
    with get_openai_callback() as cb:
        async for chunk in llm.astream(
            [*llm_context, HumanMessage(content=message.content)], stream_usage=True
        ):
            if not chunk.content:
                continue
            chunk_content = chunk.content
            if not isinstance(chunk_content, str):
                # TODO: don't output dict content when type handled
                logger.error(f"Chunk content is not a string {chunk_content}")
                continue
            # strip leading new line on the start of the message
            # TODO: use langchain BaseChunk merging
            chunks.append(chunk_content.lstrip()) if len(
                chunks
            ) == 0 else chunks.append(chunk_content)
            await redis.publish(
                topic,
                ChatMessageSSE(
                    id=new_message_id, content=chunk_content
                ).model_dump_json(),
            )
    logger.info(f"OpenAI tokens used: {cb.total_tokens:_}, cost: {cb.total_cost:.3f}$")
    new_message = await chat_svc.create_chat_message(
        chat_id=message.chat_id,
        message="".join(chunks),
        role=ChatMessageRole.ASSISTANT,
    )
    debug("".join(chunks))

    await redis.publish(
        topic,
        ChatMessageEndSSE(
            id=new_message_id,
            new_id=new_message.id,
            created_at=new_message.created_at,
            content=new_message.content,
        ).model_dump_json(),
    )


async def get_llm_context(
    db_session: AsyncSession, document_ids: list[UUID], message: ChatMessageModel
) -> list[SystemMessage | HumanMessage | AIMessage]:
    rag = await get_rag(document_ids, message.user_id, message.content)
    llm_context: list[SystemMessage | HumanMessage | AIMessage]
    if not rag:
        llm_context = [
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(content=message.content),
            HumanMessage(
                content="Tell the user that you don't have needful data to provide the answer."
            ),
        ]
    else:
        llm_context = [
            SystemMessage(SYSTEM_PROMPT),
            *await get_prompts_examples(message),
            *rag,
            HumanMessage(content=message.content),
        ]

    debug(llm_context)
    return list(llm_context)


async def get_history(
    db_session: AsyncSession, message: ChatMessageModel, limit: int = 15
) -> list[AIMessage]:
    """
    Retrieves last messages from the chat to provide context to the LLM.
    """
    async with db_session.begin():
        result = await db_session.execute(
            sql.select(ChatMessageModel)
            .filter_by(chat_id=message.chat_id, deleted_at=None)
            .where(
                ChatMessageModel.created_at < message.created_at,
            )
            .order_by(ChatMessageModel.created_at.desc())
            .limit(limit)
        )
    messages = result.scalars().all()
    return [AIMessage(content=message.content) for message in messages]


async def get_prompts_examples(message: ChatMessageModel) -> list[SystemMessage]:
    wvc = get_weaviate_client(with_openai=True)
    await wvc.connect()
    try:
        collection = wvc.collections.get("Prompts")
        response = await collection.query.near_text(
            query=message.content,
            certainty=0.5,
            limit=10,
        )
        return [
            SystemMessage(f"""
        Example of response you provide:
        {"\n".join([f"- {prompt.properties["reply"]}" for prompt in response.objects])}
        """)
        ]
    finally:
        await wvc.close()
