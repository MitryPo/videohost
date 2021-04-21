from enum import unique
import ormar
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from db import MainMeta
from user.schemas import UserDB


class User(OrmarBaseUserModel):
    class Meta(MainMeta):
        pass

    username: str = ormar.String(max_length=50, unique=True)
    phone: str = ormar.String(max_length=12, unique=True)

user_db = OrmarUserDatabase(UserDB, User)