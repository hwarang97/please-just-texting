from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


# create user
class UserCreate(BaseModel):
    name: str
    password: str
    user_email: EmailStr


# update user
class UpdateUser(BaseModel):
    name: str = Field(default=None)
    password: str = Field(default=None)
    user_email: EmailStr = Field(default=None)


# search user
class UserResponse(BaseModel):
    id: int
    name: str
    user_email: EmailStr

    class Config:
        from_attributes = True
