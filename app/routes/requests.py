from typing import List, Tuple
from fastapi import APIRouter, Depends
from app.database.config import session
from app.database.models import Request
from app.models.pydantic_models import (
    RequestCreateModel,
    RequestDB,
    RequestPublicModel,
    RequestUpdateModel,
)
from app.utils.pagination import pagination
from app.utils.dependencies import get_entity_or_404

router = APIRouter()


@router.get("/")
async def get_requests(
    pagination: Tuple[int, int] = Depends(pagination)
) -> List[RequestDB]:
    skip, limit = pagination
    requests = session.query(Request).limit(limit).offset(skip).all()
    result = [RequestDB.from_orm(request) for request in requests]

    return result


@router.get("/{id}")
async def get_request(id: int) -> RequestPublicModel:
    request = await get_entity_or_404(
        id=id, class_entity=Request, pydantic_model=RequestPublicModel
    )

    return request


@router.post("/")
async def create_request(create_request: RequestCreateModel) -> RequestPublicModel:
    request_instance = Request(**create_request.dict())

    session.add(request_instance)
    session.commit()

    new_request = await get_entity_or_404(
        id=request_instance.id,
        class_entity=Request,
        pydantic_model=RequestPublicModel,
    )

    return new_request


@router.patch("/{id}")
async def update_request(
    id: int, update_request: RequestUpdateModel
) -> RequestPublicModel:
    session.query(Request).filter(Request.id == id).update(
        update_request.dict(exclude_unset=True)
    )

    session.commit()
    udated_request = await get_entity_or_404(
        id=id,
        class_entity=Request,
        pydantic_model=RequestPublicModel,
    )

    return udated_request


@router.delete("/{id}")
async def delete_request(id: int) -> None:
    session.query(Request).filter(Request.id == id).delete()
    session.commit()
    return None
