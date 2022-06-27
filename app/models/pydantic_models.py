from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.utils.departments import Department


class Received(str, Enum):
    SI = "SI"
    NO = "NO"
    PARCIAL = "PARCIAL"


def convert_to_lowercase(n: str):
    return n.lower().strip()

# list of providers
class ListProviders(BaseModel):
    id: int

    class Config:
        orm_mode = True


# Admin Pydantic Model ###########################################
class AdministratorBaseModel(BaseModel):
    name: str
    last_name: str
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class AdministratorDB(AdministratorBaseModel):
    id: int


class AdministratorCreateModel(AdministratorBaseModel):
    password: str

    _name = validator("name", allow_reuse=True)(convert_to_lowercase)
    _last_name = validator("last_name", allow_reuse=True)(convert_to_lowercase)


class AdministratorPublicModel(AdministratorBaseModel):
    password_hash: str


class AdministratorUpdateModel(AdministratorCreateModel):
    name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    last_seen: Optional[datetime]
    update_date: datetime = Field(default_factory=datetime.now)


# Request Pydantic Model ####################################################
class RequestBaseModel(BaseModel):
    requester_id: int
    request_number: str = Field(...)
    description: str
    received: Received = Field(default=Received.NO)
    comments: str
    requested_at: datetime
    purchase_order_number: str = Field(...)
    created_by_id: int
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class RequestDB(RequestBaseModel):
    id: int


class RequestUpdateModel(RequestBaseModel):
    requester_id: Optional[int]
    request_number: Optional[str] = Field(...)
    description: Optional[str]
    comments: Optional[str]
    requested_at: Optional[datetime]
    created_by_id: Optional[int]
    received: Optional[Received]
    purchase_order_number: Optional[str] = Field(...)
    providers: Optional[List[ListProviders]]
    updated_by_id: int
    update_date: datetime = Field(default_factory=datetime.now)
    # Funtion to clean data
    _request_number = validator("request_number", allow_reuse=True)(
        convert_to_lowercase
    )
    _description = validator("description", allow_reuse=True)(convert_to_lowercase)
    _comments = validator("comments", allow_reuse=True)(convert_to_lowercase)
    _purchase_order_number = validator("purchase_order_number", allow_reuse=True)(
        convert_to_lowercase
    )


class ListRequestsModel(BaseModel):
    id: int
    request_number: str

    class Config:
        orm_mode = True


# Providers Pydantic Model ##################################################
class ProviderBaseModel(BaseModel):
    name: str
    created_by_id: int
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class ProviderDB(ProviderBaseModel):
    id: int


class ProviderCreateModel(ProviderBaseModel):
    _name = validator("name", allow_reuse=True)(convert_to_lowercase)


class ProviderPublicModel(ProviderDB):
    requests: List[ListRequestsModel]


class ProviderUpdateModel(ProviderBaseModel):
    created_by_id: Optional[int]
    updated_by_id: int
    update_date: datetime = Field(default_factory=datetime.now)


# Requester Pydantic Model #########################################################
class RequesterBaseModel(BaseModel):
    name: str
    last_name: str
    work_as: str
    department: Department = Field(default=Department.NO_DEPARTMENT)
    created_by_id: int
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class RequesterDB(RequesterBaseModel):
    id: int


class RequesterCreateModel(RequesterBaseModel):
    _name = validator("name", allow_reuse=True)(convert_to_lowercase)
    _last_name = validator("last_name", allow_reuse=True)(convert_to_lowercase)
    _work_as = validator("work_as", allow_reuse=True)(convert_to_lowercase)


class RequesterPublicModel(RequesterDB):
    requests: List[ListRequestsModel]



class RequesterUpdateModel(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    work_as: Optional[str]
    department: Optional[Department]
    updated_by_id: int
    update_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


# Another classes of request
class RequestCreateModel(RequestBaseModel):
    providers: Optional[List[ListProviders]]
    
    _request_number = validator("request_number", allow_reuse=True)(
        convert_to_lowercase
    )
    _description = validator("description", allow_reuse=True)(convert_to_lowercase)
    _comments = validator("comments", allow_reuse=True)(convert_to_lowercase)
    _purchase_order_number = validator("purchase_order_number", allow_reuse=True)(
        convert_to_lowercase
    )


class RequestPublicModel(RequestCreateModel):
    pass
