from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserSigninModel(BaseModel):
    name: str
    password: str


class UserCreateModel(BaseModel):
    name: str
    password: str
    email: EmailStr


class RecoveryModel(BaseModel):
    email: EmailStr


class PasswordModel(BaseModel):
    name: str
    email: EmailStr
    new_password: str


class DeleteModel(BaseModel):
    name: str
    password: str
    email: EmailStr


class ConversationModel(BaseModel):
    message: str = Field(...)


class UserModel(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserResponseModel(BaseModel):
    result: str
    name: str | None = None
    email: str | None = None
    error: str | None = None


class ConversationResponseModel(BaseModel):
    schedule_response: str | None = None
    parsed_response: dict
