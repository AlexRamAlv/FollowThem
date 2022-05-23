from typing import List
from fastapi import APIRouter

from app.models.admin import AdministratorDB, AdministratorPublicModel

router = APIRouter()


@router.get("/")
def get_admins() -> List[AdministratorDB]:
    pass


@router.get("/{id}")
def get_admin() -> AdministratorPublicModel:
    pass


@router.post("/")
def create_admin() -> AdministratorPublicModel:
    pass


@router.patch("/{id}")
def update_admin() -> AdministratorPublicModel:
    pass


@router.delete("/{id}")
def delete_admin() -> None:
    pass
