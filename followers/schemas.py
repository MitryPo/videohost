from pydantic import BaseModel
from typing import List
from user.schemas import UserOut


class FollowerCreate(BaseModel):
    username: str


class FollowerList(BaseModel):
    subscriber: UserOut


class FollowingList(BaseModel):
    user: UserOut