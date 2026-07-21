from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship # 需要引入原生 relationship
from typing import TYPE_CHECKING
def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

# 加上这几行，只给编辑器/类型检查器看
if TYPE_CHECKING:
    from app.items.models import Item
    from app.tasks.models import Task

# 共享属性
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# 注册时前端传来的数据校验
class UserRegister(SQLModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

# 创建用户时的数据校验（管理员创建）
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# 更新用户时的数据校验
class UserUpdate(UserBase):
    email: str | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

# 更新自身密码时的数据校验
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# 重置密码时的数据校验
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

# 数据库表模型
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # 修改这行：明确把目标模型的字符串 "Item" 传给 Relationship
    items: list["Item"] = Relationship(
        sa_relationship=relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    )
    tasks: list["Task"] = Relationship(
        sa_relationship=relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    )

# API 返回给前端的用户数据（过滤掉密码）
class UserPublic(UserBase):
    id: UUID

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int