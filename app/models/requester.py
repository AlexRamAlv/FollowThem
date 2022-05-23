from datetime import datetime
from typing import Optional
from app.utils.departments import Department
from pydantic import BaseModel, Field


class RequesterBaseModel(BaseModel):
    name: str
    last_name: str
    work_as: str
    department: Department
    created_by: int

    class config:
        orm_mode = True


class RequesterDB(RequesterBaseModel):
    id: int


class RequesterCreateModel(RequesterBaseModel):
    creation_date: datetime = Field(default_factory=datetime.now())


class RequesterPublicModel(RequesterBaseModel):
    pass


class RequesterUpdateModel(RequesterBaseModel):
    name: Optional[str]
    last_name: Optional[str]
    work_as: Optional[str]
    department: Optional[Department]
    updated_by: int
    updated_date: datetime = Field(default_factory=datetime.now())
