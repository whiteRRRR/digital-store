from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)
from typing import Annotated

from pydantic_extra_types.phone_numbers import PhoneNumber


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: Annotated[str, Field(title="username", min_length=3, max_length=30)]
    first_name: Annotated[str, Field(title="first_name", min_length=3, max_length=30)]
    last_name: Annotated[str, Field(title="last_name", min_length=3, max_length=30)]
    email: EmailStr
    phone_number: PhoneNumber
    is_active: bool = True


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]


class UserInDataBase(UserBase):
    password: bytes






