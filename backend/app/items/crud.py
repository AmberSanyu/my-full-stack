import uuid
from sqlmodel import Session, select, func, col
from app.models import Item, ItemCreate, ItemUpdate

def get_items(*, session: Session, owner_id: uuid.UUID | None = None, skip: int = 0, limit: int = 100):
    """根据参数获取列表，如果传入 owner_id 则过滤用户"""
    # 查总数
    count_stmt = select(func.count()).select_from(Item)
    if owner_id:
        count_stmt = count_stmt.where(Item.owner_id == owner_id)
    count = session.exec(count_stmt).one()

    # 查列表
    stmt = select(Item).order_by(col(Item.created_at).desc()).offset(skip).limit(limit)
    if owner_id:
        stmt = stmt.where(Item.owner_id == owner_id)
    items = session.exec(stmt).all()

    return items, count

def get_item(*, session: Session, item_id: uuid.UUID) -> Item | None:
    return session.get(Item, item_id)

def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def update_item(*, session: Session, db_item: Item, item_in: ItemUpdate) -> Item:
    update_dict = item_in.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(update_dict)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def delete_item(*, session: Session, db_item: Item) -> None:
    session.delete(db_item)
    session.commit()