from typing import List, Tuple
from fastapi import APIRouter, Depends, status, Response
from app.database.config import session
from app.database.models import Request, Requester, Administrator, Provider
from app.models.pydantic_models import (
    RequestCreateModel,
    RequestDB,
    RequestPublicModel,
    RequestUpdateModel,
    AdministratorDB,
    RequesterDB,
    ProviderDB
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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_request(create_request: RequestCreateModel) -> RequestPublicModel:
    create_request_dict = create_request.dict()

    await get_entity_or_404(
        id=create_request_dict["created_by_id"],
        class_entity=Administrator,
        pydantic_model=AdministratorDB,
    )

    await get_entity_or_404(
        id=create_request_dict["requester_id"],
        class_entity=Requester,
        pydantic_model=RequesterDB,
    )

    providers = create_request_dict.get("providers")
    del create_request_dict["providers"]
    request_instance = Request(**create_request_dict)
    
    if providers:
        for p in providers:
            await get_entity_or_404(
                id=p["id"],
                class_entity=Provider,
                pydantic_model=ProviderDB,
            )
            provier_in_db = session.query(Provider).get(p["id"])
            request_instance.providers.append(provier_in_db)

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

    request = session.query(Request)
    requet_to_be_update = request.get(id)
    update_request_info = update_request.dict(exclude_unset=True)
    providers = update_request_info.get("providers")
    
    if providers:
        requet_to_be_update.providers.clear()
        for p in providers:
            await get_entity_or_404(
                id=p["id"],
                class_entity=Provider,
                pydantic_model=ProviderDB,
            )
            provier_in_db = session.query(Provider).get(p["id"])
            requet_to_be_update.providers.append(provier_in_db)

        del update_request_info["providers"]

    request.filter(Request.id == id).update(
        update_request_info
    )

    session.commit()
    udated_request = await get_entity_or_404(
        id=id,
        class_entity=Request,
        pydantic_model=RequestPublicModel,
    )

    return udated_request


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_request(id: int) -> None:
    await get_entity_or_404(
        id=id,
        class_entity=Request,
        pydantic_model=RequestPublicModel,
    )
    session.query(Request).filter(Request.id == id).delete()
    session.commit()
    return None
