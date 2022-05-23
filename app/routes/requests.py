from typing import List
from fastapi import APIRouter

from app.models.request import RequestDB, RequestPublicModel

router = APIRouter()


@router.get("/")
def get_requests() -> List[RequestDB]:
    pass


@router.get("/{id}")
def get_request() -> List[RequestPublicModel]:
    pass


@router.post("/")
def create_request() -> List[RequestPublicModel]:
    pass


@router.patch("/{id}")
def update_request() -> List[RequestPublicModel]:
    pass


@router.delete("/{id}")
def delete_request() -> None:
    pass
