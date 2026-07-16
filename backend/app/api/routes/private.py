from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

# 引入抽离后的用户专属数据访问层
from app.users import crud
from app.api.deps import SessionDep
from app.models import UserPublic

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user via private channel.
    """
    # 视图层清晰干净，只负责中转数据
    user = crud.create_private_user(
        session=session,
        email=user_in.email,
        full_name=user_in.full_name,
        password=user_in.password
    )
    return user