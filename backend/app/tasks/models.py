from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# 基础模型（用于前端传输和校验，不建表）
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: str = Field(default="todo")  # todo, doing, done

# 数据库表模型（真正对应数据库的表）
class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.timezone.utcnow)
    update_at: datetime = Field(default_factory=datetime.timezone.utcnow)
    
    # 外键：关联到 User 表
    owner_id: UUID = Field(foreign_key="user.id", nullable=False)
    
    # 关系属性：在 Python 代码中可以直接通过 task.owner 拿到 User 对象
    owner: "User" = Relationship(back_populates="tasks")