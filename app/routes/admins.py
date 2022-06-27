from typing import List, Tuple
from fastapi import APIRouter, Depends, Response, status
from app.utils.dependencies import get_entity_or_404
from app.database.models import Administrator
from app.database.config import session
from app.models.pydantic_models import (
    AdministratorCreateModel,
    AdministratorDB,
    AdministratorPublicModel,
    AdministratorUpdateModel,
)
from app.utils.pagination import pagination

router = APIRouter()


@router.get("/")
async def get_admins(
    pagination: Tuple[int, int] = Depends(pagination)
) -> List[AdministratorDB]:
    skip, limit = pagination
    admins = session.query(Administrator).limit(limit).offset(skip).all()
    result = [AdministratorDB.from_orm(admin) for admin in admins]

    return result


@router.get("/{id}", response_model=AdministratorDB)
async def get_admin(id: int) -> AdministratorPublicModel:
    admin = await get_entity_or_404(
        id=id, class_entity=Administrator, pydantic_model=AdministratorDB
    )

    return admin


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AdministratorPublicModel
)
async def create_admin(admin: AdministratorCreateModel) -> AdministratorPublicModel:
    admin_instance = Administrator(**admin.dict())

    session.add(admin_instance)
    session.commit()

    new_admin = await get_entity_or_404(
        id=admin_instance.id,
        class_entity=Administrator,
        pydantic_model=AdministratorPublicModel,
    )

    return new_admin


@router.patch("/{id}", response_model=AdministratorPublicModel)
async def update_admin(
    id: int, update_admin: AdministratorUpdateModel
) -> AdministratorPublicModel:

    session.query(Administrator).filter(Administrator.id == id).update(
        update_admin.dict(exclude_unset=True)
    )

    session.commit()
    udated_admin = await get_entity_or_404(
        id=id,
        class_entity=Administrator,
        pydantic_model=AdministratorPublicModel,
    )

    return udated_admin


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_admin(id: int) -> None:
    await get_entity_or_404(
        id=id,
        class_entity=Administrator,
        pydantic_model=AdministratorPublicModel,
    )
    session.query(Administrator).filter(Administrator.id == id).delete()
    session.commit()
    return None
