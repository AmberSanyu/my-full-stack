from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import CurrentUser, get_db
from app.models import TaskPublic, TaskUpdate

# 导入你刚刚在上面写好的 crud 逻辑
from app.tasks import crud as task_crud

router = APIRouter(prefix="/tasks", tags=["tasks"])  # 👈 确保这里有 tags

@router.patch("/{task_no}", response_model=TaskPublic)
def update_task_route(
    *,
    session: Session = Depends(get_db),
    task_no: str,
    task_in: TaskUpdate,
    current_user: CurrentUser,
):
    """
    业务逻辑：通过业务 ID (task_no) 更新指定的任务
    """
    # 1. 业务逻辑：先调用 CRUD 查出这条数据
    db_task = task_crud.get_task_by_no(session=session, task_no=task_no)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="找不到该任务"
        )
        
    # 2. 权限校验：非管理员只能修改自己名下的任务
    if not current_user.is_superuser and db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="你没有权限修改此任务"
        )
        
    # 3. 业务逻辑：调用 CRUD 执行更新
    updated_task = task_crud.update_task_by_no(
        session=session, db_task=db_task, task_in=task_in
    )
    
    # 这里的返回对象 updated_task 依然包含真实的 id，
    # 但由于装饰器指定了 response_model=TaskPublic，FastAPI 会在返回时自动把 id 剔除，只留下 task_no
    return updated_task