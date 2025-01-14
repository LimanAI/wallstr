import hashlib
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

import sqlalchemy
from pydantic import EmailStr, HttpUrl
from sqlalchemy import LargeBinary, MetaData, String, TypeDecorator
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, mapped_column
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import EmailType


def utc_now() -> datetime:
    return datetime.now(UTC)


"""
https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-a-naming-convention-for-a-metadata-collection

pkey for a Primary Key constraint
key for a Unique constraint
excl for an Exclusion constraint
idx for any other kind of index
fkey for a Foreign key
check for a Check constraint
seq for all sequences
"""
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_N_label)s",
        "uq": "uq_%(table_name)s__%(column_0_N_name)s",
        "ck": "ck_%(table_name)s__%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(referred_table_name)s__%(column_0_N_name)s",
        "pk": "pk_%(table_name)s",
    }
)

# See https://github.com/dropbox/sqlalchemy-stubs/issues/94
PostgresUUID = cast(
    sqlalchemy.types.TypeEngine[UUID],
    postgresql.UUID(as_uuid=True),
)


class HashType(TypeDecorator[str]):
    impl = LargeBinary(64)
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect: Dialect) -> bytes | None:
        if value is None:
            return None
        return hashlib.sha512(value.encode()).digest()

    def process_result_value(self, value: bytes | None, dialect: Dialect) -> str | None:
        if value is None:
            return None
        return value.hex()


def string_column(
    length: int, nullable: bool = False, default: str | None = "", **kwargs: Any
) -> Any:
    """
    Factory for creating string columns with sane defaults.

    This follows the convention of avoiding NULL for string columns.
    Instead, an empty string is used as the default value when the column is not nullable.
    """
    return mapped_column(String(length), nullable=nullable, default=default, **kwargs)


class BaseModel(DeclarativeBase):
    __abstract__ = True
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
        HttpUrl: String(4096),
        EmailStr: EmailType(),
        UUID: PostgresUUID,
    }

    metadata = metadata


class TimestampModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=utc_now, default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)


class RecordModel(TimestampModel):
    __abstract__ = True

    id: MappedColumn[UUID] = mapped_column(
        PostgresUUID, primary_key=True, default=uuid4
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}(id='{self.id}')"
        )