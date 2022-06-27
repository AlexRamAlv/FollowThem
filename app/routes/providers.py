from typing import List, Tuple
from fastapi import APIRouter, Depends, status, Response
from app.database.config import session
from app.database.models import Provider, Administrator
from app.models.pydantic_models import (
    ProviderCreateModel,
    ProviderDB,
    ProviderPublicModel,
    ProviderUpdateModel,
    AdministratorDB
)
from app.utils.dependencies import get_entity_or_404
from app.utils.pagination import pagination


router = APIRouter()


@router.get("/")
async def get_providers(
    pagination: Tuple[int, int] = Depends(pagination)
) -> List[ProviderDB]:
    skip, limit = pagination
    providers = session.query(Provider).limit(limit).offset(skip).all()
    result = [ProviderDB.from_orm(provider) for provider in providers]

    return result


@router.get("/{id}", response_model=ProviderPublicModel)
async def get_provider(id: int) -> ProviderPublicModel:
    provider = await get_entity_or_404(
        id=id, class_entity=Provider, pydantic_model=ProviderPublicModel
    )

    return provider


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProviderDB)
async def create_provider(provider: ProviderCreateModel) -> ProviderDB:
    provider_instance = Provider(**provider.dict())

    await get_entity_or_404(
        id=provider_instance.created_by_id,
        class_entity=Administrator,
        pydantic_model=AdministratorDB,
    )

    session.add(provider_instance)
    session.commit()

    new_provider = await get_entity_or_404(
        id=provider_instance.id,
        class_entity=Provider,
        pydantic_model=ProviderDB,
    )

    return new_provider


@router.patch("/{id}", response_model=ProviderDB)
async def update_provider(id: int, update_provider: ProviderUpdateModel) -> ProviderDB:
    session.query(Provider).filter(Provider.id == id).update(
        update_provider.dict(exclude_unset=True)
    )

    session.commit()
    updated_provider = await get_entity_or_404(
        id=id,
        class_entity=Provider,
        pydantic_model=ProviderDB,
    )

    return updated_provider


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_provider(id: int) -> None:
    await get_entity_or_404(
        id=id,
        class_entity=Provider,
        pydantic_model=ProviderDB,
    )
    session.query(Provider).filter(Provider.id == id).delete()
    session.commit()
    return None
