from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
from app.database.config import session
from sqlalchemy.orm.decl_api import DeclarativeMeta


async def get_entity_or_404(
    id: int, class_entity: DeclarativeMeta, pydantic_model: BaseModel
) -> Optional[BaseModel]:

    entity = session.query(class_entity).filter_by(id=id).first()

    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the {class_entity} id {id} does not exist!",
        )

    return pydantic_model.from_orm(entity)
