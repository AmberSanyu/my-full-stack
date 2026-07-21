import uuid
from typing import Sequence
from sqlmodel import Session, select, func, col, delete
from app.models import Task, TaskCreate, TaskUpdate


def get_tasks(*, session: Session, skip: int = 0, limit: int = 100) -> tuple[Sequence[Task], int]:
    # 查总数
    count_statement = select(func.count()).select_from(Task)
    count = session.exec(count_statement).one()
    # 查列表
    statement = select(Task).order_by(col(Task.created_at).desc()).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks, count

def get_task(*, session: Session, task_id: uuid.UUID) -> Task | None:
    return session.get(Task, task_id)

def create_task(*, session: Session,task_in: TaskCreate, owner_id: uuid.UUID) -> Task:
    db_task = Task.model_validate(task_in, update={"owner_id": owner_id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def update_task(*, session: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    update_dict = task_in.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(update_dict)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(*, session: Session, db_task: Task) -> None:
    session.delete(db_task)

def get_task_by_no(*, session: Session, task_no: str) -> Task | None:
    """根据业务 ID 查询 Task 详情"""
    statement = select(Task).where(Task.task_no == task_no)
    return session.exec(statement).first()

def create_task_with_owner(*, session: Session, task_in: TaskCreate, owner_id: uuid.UUID) -> Task:
    """创建 Task（会自动触发默认的 task_no 生成规则）"""
    db_obj = Task.model_validate(task_in, update={"owner_id": owner_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_task_by_no(*, session: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    """传入查出来的 db 对象和更新 DTO，隐式利用内部绑定的真实主键进行更新"""
    # 过滤掉前端没有传的字段 (None)
    update_data = task_in.model_dump(exclude_unset=True)
    
    for field in update_data:
        setattr(db_task, field, update_data[field])
        
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task