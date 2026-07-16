import uuid
from typing import Sequence
from sqlmodel import Session, select, func, col, delete
from app.core.security import get_password_hash
from app.models import User, Item, UserCreate, UserUpdate, UserUpdateMe

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"

# 确保在 app/users/crud.py 中包含此函数
def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    from app.core.security import verify_password
    verified, _ = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    return db_user

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_user_by_id(*, session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)

def get_users(*, session: Session, skip: int = 0, limit: int = 100) -> tuple[Sequence[User], int]:
    # 查总数
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    # 查列表
    statement = select(User).order_by(col(User.created_at).desc()).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users, count

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_user(*, session: Session, db_user: User, user_in: UserUpdate | UserUpdateMe) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if isinstance(user_in, UserUpdate) and user_in.password:
        user_data["hashed_password"] = get_password_hash(user_in.password)
        del user_data["password"]
        
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user_password(*, session: Session, db_user: User, new_password: str) -> None:
    db_user.hashed_password = get_password_hash(new_password)
    session.add(db_user)
    session.commit()

def delete_user(*, session: Session, db_user: User) -> None:
    # 级联删除该用户的 items 记录
    item_delete_statement = delete(Item).where(col(Item.owner_id) == db_user.id)
    session.exec(item_delete_statement)
    # 删除用户本身
    session.delete(db_user)
    session.commit()

# 确保在 app/users/crud.py 中追加此函数
def create_private_user(*, session: Session, email: str, full_name: str, password: str) -> User:
    """内部私有渠道创建用户，直接生成哈希密码并写入数据库"""
    db_obj = User(
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj