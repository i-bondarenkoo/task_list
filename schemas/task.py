from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.tag import ResponseTag
    from schemas.user import ResponseUser


class CreateTask(BaseModel):
    title: str
    description: str
    user_id: int


class ResponseTask(CreateTask):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseTaskWithRelationship(BaseModel):
    id: int
    title: str
    description: str
    # user: "ResponseUser"
    user_id: int
    tags: list["ResponseTag"]
    model_config = ConfigDict(from_attributes=True)


class UpdatePartialTask(BaseModel):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
