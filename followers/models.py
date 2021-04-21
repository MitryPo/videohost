import ormar
from typing import Dict, Optional, Union
from user.models import User
from db import MainMeta


class Follower(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[User, Dict]]= ormar.ForeignKey(User, related_name="user")
    subscriber: Optional[Union[User, Dict]]= ormar.ForeignKey(User, related_name="subscriber")