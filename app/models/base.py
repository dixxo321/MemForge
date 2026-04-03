from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)


class BaseRecord(TimestampedModel):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    archived_at: Optional[datetime] = Field(default=None, nullable=True)
    metadata_json: Optional[str] = Field(default=None, nullable=True)
