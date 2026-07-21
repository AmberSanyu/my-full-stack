import uuid
from typing import Sequence
from sqlmodel import Session, func, select

from app.tasks.models import Task, TaskCreate, TaskUpdate


# ==========================================
# 1. 查询类 (Read)
# ==========================================

def get_task_by_no(*, session: Session, task_no: str) -> Task | None:
    """
    通过业务编号 (task_no) 查询单条任务数据
    """
    statement = select(Task).where(Task.task_no == task_no)
    return session.exec(statement).first()


def get_task_by_id(*, session: Session, task_id: uuid.UUID) -> Task | None:
    """
    通过数据库主键 ID (id) 查询单条任务数据
    """
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()


def get_tasks_by_owner(
    *,
    session: Session,
    owner_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[Task], int]:
    """
    获取指定用户的任务列表（支持分页），并返回 (任务列表, 总条数)
    """
    # 1. 查询列表数据
    statement = (
        select(Task)
        .where(Task.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    tasks = session.exec(statement).all()

    # 2. 查询总条数
    count_statement = (
        select(func.count())
        .select_from(Task)
        .where(Task.owner_id == owner_id)
    )
    count = session.exec(count_statement).one()

    return tasks, count


def get_tasks(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 100,
) -> tuple[Sequence[Task], int]:
    """
    管理员模式：获取全量任务列表（支持分页），并返回 (任务列表, 总条数)
    """
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()

    count_statement = select(func.count()).select_from(Task)
    count = session.exec(count_statement).one()

    return tasks, count


# ==========================================
# 2. 新增类 (Create)
# ==========================================

def create_task_with_owner(
    *,
    session: Session,
    task_in: TaskCreate,
    owner_id: uuid.UUID,
) -> Task:
    """
    创建绑定到具体用户的任务
    """
    db_obj = Task.model_validate(task_in, update={"owner_id": owner_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# ==========================================
# 3. 更新类 (Update)
# ==========================================

def update_task_by_no(
    *,
    session: Session,
    db_task: Task,
    task_in: TaskUpdate,
) -> Task:
    """
    更新已存在的 Task 实例对象（只更新传入的非空字段）
    """
    update_data = task_in.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(update_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


# ==========================================
# 4. 删除类 (Delete)
# ==========================================

def delete_task_by_no(*, session: Session, db_task: Task) -> None:
    """
    从数据库中直接删除 Task 实例对象
    """
    session.delete(db_task)
    session.commit()