from typing import List
from fastapi import APIRouter

from app.models.provider import ProviderDB, ProviderPublicModel


router = APIRouter()


@router.get("/")
def get_providers() -> List[ProviderDB]:
    pass


@router.get("/{id}")
def get_provider() -> ProviderPublicModel:
    pass


@router.post("/")
def create_provider() -> ProviderPublicModel:
    pass


@router.patch("/{id}")
def update_provider() -> ProviderPublicModel:
    pass


@router.delete("/{id}")
def delete_provider() -> None:
    pass
