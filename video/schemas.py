from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str


class GetListVideo(BaseModel):
    id: int
    title: str
    description: str


class GetVideo(GetListVideo):
    user: User
