from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.task import ResponseTask


class CreateTag(BaseModel):
    name: str
    color: str


class ResponseTag(CreateTag):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseTagWithRelationship(BaseModel):
    id: int
    name: str
    color: str
    tasks: list["ResponseTask"]


class UpdatePartialTag(BaseModel):
    name: str | None = None
    color: str | None = None
