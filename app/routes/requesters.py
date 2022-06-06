from typing import List, Tuple
from fastapi import APIRouter, Depends, Response, status
from app.models.pydantic_models import (
    RequesterCreateModel,
    RequesterDB,
    RequesterPublicModel,
    RequesterUpdateModel,
)
from app.utils.dependencies import get_entity_or_404
from app.utils.pagination import pagination
from app.database.config import session
from app.database.models import Requester


router = APIRouter()


@router.get("/")
async def get_requester(
    pagination: Tuple[int, int] = Depends(pagination)
) -> List[RequesterDB]:
    skip, limit = pagination
    requesters = session.query(Requester).limit(limit).offset(skip).all()
    result = [RequesterDB.from_orm(requester) for requester in requesters]

    return result


@router.get("/{id}")
async def get_requester(id: int) -> RequesterPublicModel:
    requester = await get_entity_or_404(
        id=id, class_entity=Requester, pydantic_model=RequesterPublicModel
    )

    return requester


@router.post("/", response_model=RequesterDB, status_code=status.HTTP_201_CREATED)
async def create_requester(create_requester: RequesterCreateModel) -> RequesterDB:
    requester_instance = Requester(**create_requester.dict())

    session.add(requester_instance)
    session.commit()

    new_requester = await get_entity_or_404(
        id=requester_instance.id,
        class_entity=Requester,
        pydantic_model=RequesterDB,
    )

    return new_requester


@router.patch("/{id}")
async def update_requester(
    id: int, update_requester: RequesterUpdateModel
) -> RequesterPublicModel:
    session.query(Requester).filter(Requester.id == id).update(
        update_requester.dict(exclude_unset=True)
    )

    session.commit()
    udated_requester = await get_entity_or_404(
        id=id,
        class_entity=Requester,
        pydantic_model=RequesterPublicModel,
    )

    return udated_requester


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_requester(id: int) -> None:
    session.query(Requester).filter(Requester.id == id).delete()
    session.commit()
    return None
