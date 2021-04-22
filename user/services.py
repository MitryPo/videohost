from fastapi import HTTPException
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from . import schemas, models, tokenizator


GOOGLE_CLIENT_ID = "575180527966-97oaqa2gm69vac5ltsddm19rqfn301jp.apps.googleusercontent.com"


def on_after_register(user: schemas.UserOut):
    if not os.path.isdir(f"media/{user.id}"):
        os.mkdir(f"media/{user.id}")


async def create_user(user: schemas.UserCreate) -> models.User:
    _user = await models.User.objects.get_or_create(**user.dict(exclude={"token"}))
    on_after_register(_user)
    return _user


async def google_auth(user: schemas.UserCreate) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(
            user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    internal_token = tokenizator.create_token(user.id)
    return user.id, internal_token.get("access_token")
