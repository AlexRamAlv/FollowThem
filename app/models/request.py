from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.provider import ProviderDB


class Received(str, Enum):
    SI = "SI"
    NO = "NO"
    PARCIAL = "PARCIAL"


class RequestBaseModel(BaseModel):
    requester_id: int
    request_number: str = Field(...)
    description: str
    comments: str
    requested_at: datetime
    received: Received
    purchase_order_number: str = Field(...)
    created_by: int
    creation_date: datetime = Field(default_factory=datetime.now())

    class config:
        orm_mode = True


class RequestDB(RequestBaseModel):
    id: int


class RequestCreateModel(RequestBaseModel):
    providers: List[ProviderDB]


class RequestPublicModel(RequestBaseModel):
    pass


class RequestUpdateModel(RequestBaseModel):
    requester_id: Optional[int]
    request_number: Optional[str] = Field(...)
    description: Optional[str]
    comments: Optional[str]
    requested_at: Optional[datetime]
    received: Optional[Received]
    purchase_order_number: Optional[str] = Field(...)
    updated_by: int
    updated_date: datetime = Field(default_factory=datetime.now())
    providers: Optional[List[ProviderDB]]
