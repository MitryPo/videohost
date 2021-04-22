from typing import List, Union, Dict, Optional
from user.models import User
from db import MainMeta
import datetime
import ormar


class UserLike(ormar.Model):
    class Meta(MainMeta):
        pass
    
    id: int = ormar.Integer(primary_key=True)


class Video(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=250)
    file: str = ormar.String(max_length=1000)
    create_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now)
    user: Optional[User] = ormar.ForeignKey(User)
    likes: int = ormar.Integer(default=0)
    like_user: Optional[Union[List[User], Dict]] = ormar.ManyToMany(
        User, related_name="like_user", through=UserLike
    )
