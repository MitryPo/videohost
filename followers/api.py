from fastapi import APIRouter, Depends
from . import schemas
from typing import List
from .models import Follower
from user.auth import get_user
from user.models import User


follower_router = APIRouter(prefix='/followers', tags=["followers"])


@follower_router.post('/', status_code=201)
async def add_follower(schema: schemas.FollowerCreate,
                       user: User = Depends(get_user)):

    host = await User.objects.get(username=schema.username)
    return await Follower.objects.create(
        subscriber=user.dict(), user=host)


@follower_router.get('/', response_model=List[schemas.FollowingList])
async def my_following_list(user: User = Depends(get_user)):
    print(user)
    return await Follower.objects.select_related(["user"]).filter(subscriber=user.id).all()


@follower_router.get('/my', response_model=List[schemas.FollowerList])
async def my_followers(user: User = Depends(get_user)):

    return await Follower.objects.select_related(["subscriber"]).filter(user=user.id).all()


@follower_router.delete('/{username}', status_code=204)
async def my_followers(username: str, user: User = Depends(get_user)):
    follower = await Follower.objects.get(user__username=username, subscriber=user.id)
    if follower:
        await follower.delete()
        return {"response":"ok"}
    else:
        return {"response":"Пользователь не найден"}
    
    return {}
