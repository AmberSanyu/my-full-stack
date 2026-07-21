# 1. 从各自的模块中导入所有模型
from app.users.models import (
    User,
    UserBase,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
    UpdatePassword,
    NewPassword,
)
from app.items.models import (
    Item,
    ItemBase,
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
)

from app.tasks.models import (
    Task,
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskPublic
)

# 2. 保留原有的通用公共模型
from sqlmodel import Field, SQLModel

class Message(SQLModel):
    message: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str | None = None

