from typing import Optional
from fastapi_users import models
from pydantic import BaseModel, UUID4
from pydantic.networks import EmailStr



class User(models.BaseUser):
    username: str
    phone: str

class UserCreate(models.CreateUpdateDictModel):
    email: EmailStr
    username: str
    password: str
    phone: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserOut(BaseModel):
    id: UUID4
    username: str