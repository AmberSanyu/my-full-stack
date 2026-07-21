from typing import Any
from fastapi import APIRouter, HTTPException, status
from app.api.deps import CurrentUser, SessionDep
from app.models import Message
from app.tasks.models import TaskPublic, TaskCreate, TaskUpdate, TasksPublic

# 导入你的 crud 模块
from app.tasks import crud as task_crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


# 1. 查询任务列表 (GET)
@router.get("/", response_model=TasksPublic)
def read_tasks(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取当前用户的任务列表
    """
    if current_user.is_superuser:
        # 管理员查看全部任务（需在 task_crud 中实现对应的获取所有任务方法）
        tasks, count = task_crud.get_tasks(session=session, skip=skip, limit=limit)
    else:
        # 普通用户只看自己的任务
        tasks, count = task_crud.get_tasks_by_owner(
            session=session, owner_id=current_user.id, skip=skip, limit=limit
        )

    return TasksPublic(data=tasks, count=count)


# 2. 创建任务 (POST)
@router.post("/", response_model=TaskPublic)
def create_task(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    task_in: TaskCreate,
) -> Any:
    """
    新建任务
    """
    task = task_crud.create_task_with_owner(
        session=session, task_in=task_in, owner_id=current_user.id
    )
    return task


# 3. 更新任务 (PATCH) —— 你原有的逻辑
@router.patch("/{task_no}", response_model=TaskPublic)
def update_task_route(
    *,
    session: SessionDep,
    task_no: str,
    task_in: TaskUpdate,
    current_user: CurrentUser,
) -> Any:
    """
    通过业务 ID (task_no) 更新指定任务
    """
    db_task = task_crud.get_task_by_no(session=session, task_no=task_no)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到该任务",
        )

    if not current_user.is_superuser and db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="你没有权限修改此任务",
        )

    updated_task = task_crud.update_task_by_no(
        session=session, db_task=db_task, task_in=task_in
    )
    return updated_task


# 4. 删除任务 (DELETE)
@router.delete("/{task_no}", response_model=Message)
def delete_task_route(
    *,
    session: SessionDep,
    task_no: str,
    current_user: CurrentUser,
) -> Any:
    """
    通过业务 ID (task_no) 删除指定任务
    """
    db_task = task_crud.get_task_by_no(session=session, task_no=task_no)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到该任务",
        )

    if not current_user.is_superuser and db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="你没有权限删除此任务",
        )

    task_crud.delete_task_by_no(session=session, db_task=db_task)
    return Message(message="任务删除成功")
