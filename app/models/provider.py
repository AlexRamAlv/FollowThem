from datetime import datetime
from pydantic import BaseModel, Field


class ProviderBaseModel(BaseModel):
    name: str
    created_by: int

    class config:
        orm_mode = True


class ProviderDB(ProviderBaseModel):
    id: int


class ProviderCreateModel(ProviderBaseModel):
    creation_date: datetime = Field(default_factory=datetime.now())


class ProviderPublicModel(ProviderBaseModel):
    pass


class ProviderUpdateModel(ProviderBaseModel):
    name: str
    updated_by: int
    updated_date: datetime = Field(default_factory=datetime.now())
