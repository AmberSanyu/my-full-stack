import uuid
from typing import Any
from fastapi import APIRouter, HTTPException
from app.api.deps import CurrentUser, SessionDep
from app.models import ItemPublic, ItemsPublic, ItemCreate, ItemUpdate, Message
from app.items import crud  # 引入刚才封装的层

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=ItemsPublic)
def read_items(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    # 视图层只处理业务逻辑：判断权限决定传不传 owner_id
    owner_id = None if current_user.is_superuser else current_user.id
    
    items, count = crud.get_items(session=session, owner_id=owner_id, skip=skip, limit=limit)
    
    items_public = [ItemPublic.model_validate(item) for item in items]
    return ItemsPublic(data=items_public, count=count)

@router.get("/{id}", response_model=ItemPublic)
def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    db_item = crud.get_item(session=session, item_id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 视图层核心职责：鉴权过滤
    if not current_user.is_superuser and (db_item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return db_item

@router.post("/", response_model=ItemPublic)
def create_item(*, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate) -> Any:
    return crud.create_item(session=session, item_in=item_in, owner_id=current_user.id)

@router.put("/{id}", response_model=ItemPublic)
def update_item(*, session: SessionDep, current_user: CurrentUser, id: uuid.UUID, item_in: ItemUpdate) -> Any:
    db_item = crud.get_item(session=session, item_id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (db_item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return crud.update_item(session=session, db_item=db_item, item_in=item_in)

@router.delete("/{id}")
def delete_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Message:
    db_item = crud.get_item(session=session, item_id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (db_item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    crud.delete_item(session=session, db_item=db_item)
    return Message(message="Item deleted successfully")