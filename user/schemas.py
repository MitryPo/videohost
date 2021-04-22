from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    avatar: str


class UserCreate(User):
    token: str


class UserUpdate(User):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    avatar: str


class Token(BaseModel):
    id: int
    token: str


class TokenPayload(BaseModel):
    user_id: int = None