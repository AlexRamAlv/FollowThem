from typing import List
from fastapi import APIRouter

from app.models.requester import RequesterDB, RequesterPublicModel


router = APIRouter()


@router.get("/")
def get_requester() -> List[RequesterDB]:
    pass


@router.get("/{id}")
def get_admins() -> RequesterPublicModel:
    pass


@router.post("/")
def get_requesters() -> RequesterPublicModel:
    pass


@router.patch("/{id}")
def create_requester() -> RequesterPublicModel:
    pass


@router.delete("/{id}")
def delete_requester() -> None:
    pass
