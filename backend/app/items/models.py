from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship # 需要引入原生 relationship

if TYPE_CHECKING:
    from app.users.models import User  # 仅在类型检查时导入，防止运行时循环引用

def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)
# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" | None = Relationship(
        sa_relationship=relationship("User", back_populates="items")
    )


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int