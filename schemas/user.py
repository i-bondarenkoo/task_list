from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateUserPartial(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UpdateUserFull(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
