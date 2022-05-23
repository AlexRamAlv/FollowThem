from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AdministratorBaseModel(BaseModel):
    name: str
    last_name: str
    creation_date: datetime = Field(default_factory=datetime.now())

    class config:
        orm_mode = True


class AdministratorDB(AdministratorBaseModel):
    id: int


class AdministratorCreateModel(AdministratorBaseModel):
    password_hash: str


class AdministratorPublicModel(AdministratorBaseModel):
    pass


class AdministratorUpdateModel(AdministratorBaseModel):
    name: Optional[str]
    last_name: Optional[str]
    last_seen: Optional[datetime]
    updated_at: datetime = Field(default_factory=datetime.now())
