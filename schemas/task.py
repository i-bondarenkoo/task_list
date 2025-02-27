from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    title: str
    description: str
    user_id: int


class ResponseTask(CreateTask):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdatePartialTask(BaseModel):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
