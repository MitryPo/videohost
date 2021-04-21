from user.schemas import UserDB
from starlette.requests import Request
import os

def on_after_register(user: UserDB, request: Request):
    if not os.path.isdir(f"media/{user.id}"):
        os.mkdir(f"media/{user.id}")
        print(f"User {user.id} has registered")


def send_sms(user: UserDB, request: Request) -> None:
    print(f"User {user.id} has registered. {123456}")


def after_verification(user: UserDB, token: str, request: Request) -> None:
    print(f"")