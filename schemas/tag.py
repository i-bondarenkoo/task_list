from pydantic import BaseModel, ConfigDict


class CreateTag(BaseModel):
    name: str
    color: str


class ResponseTag(CreateTag):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdatePartialTag(BaseModel):
    name: str | None = None
    color: str | None = None
