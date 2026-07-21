from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel, AutoString
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from enum import Enum
import sqlalchemy as sa
if TYPE_CHECKING:
    from app.users.models import User

def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

# 定义一个具体的业务 ID 生成规则函数
def generate_task_no() -> str:
    # 示例规则：TASK-年份月份-4位随机字母数字组合
    # 如：TASK-202607-A8B9
    current_time = get_datetime_utc().strftime("%Y%m%d%H%M%S")
    return f"TASK-{current_time}"

# 1. 定义优先级枚举
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# 基础模型（用于前端传输和校验，不建表）
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: str = Field(default="todo")  # todo, doing, done
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column=sa.Column(
            sa.Enum(
                TaskPriority,
                name="taskpriority",
                values_callable=lambda obj: [e.value for e in obj],  # 👈 映射小写字符串 value
            ),
            nullable=False,
            server_default="medium",
        ),
    )
    due_date: datetime | None = Field(default=None)

# 数据库表模型（真正对应数据库的表）
class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # 💡 新增业务 ID 字段：唯一(unique)、创建时自动生成(default_factory)、建立索引(index)方便查询
    task_no: str = Field(
        default_factory=generate_task_no, 
        unique=True, 
        index=True, 
        nullable=False,
        max_length=50
    )
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: str = Field(default="todo")  # todo, doing, done
    created_at: datetime = Field(default_factory=get_datetime_utc)
    update_at: datetime = Field(default_factory=get_datetime_utc)
    
    # 外键：关联到 User 表
    owner_id: UUID = Field(foreign_key="user.id", nullable=False)
    
    # 关系属性：在 Python 代码中可以直接通过 task.owner 拿到 User 对象
    owner: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: str | None = Field(default=None, min_length=1, max_length=255)
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    
# Properties to return via API, id is always required
class TaskPublic(TaskBase):
    id: UUID
    task_no: str
    owner_id: UUID
    created_at: datetime | None = None


class TasksPublic(SQLModel):
    data: list[TaskPublic]
    count: int