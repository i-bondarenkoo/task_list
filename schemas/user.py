from pydantic import BaseModel, EmailStr, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.task import ResponseTask, ResponseTaskWithRelationship


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseUserWithRelationship(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    tasks: list["ResponseTaskWithRelationship"]
    model_config = ConfigDict(from_attributes=True)


class UpdateUserPartial(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UpdateUserFull(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

    model_config = ConfigDict(strict=True)
