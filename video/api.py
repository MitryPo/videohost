from typing import List

from fastapi import APIRouter, File, Form, UploadFile, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from user.auth import get_user
from video.models import User, Video
from video.schemas import GetListVideo, GetVideo
from video.services import open_file, save_video

video_router = APIRouter(prefix='/video', tags=["video"])
templates = Jinja2Templates(directory="templates")


@video_router.post('/', response_model=GetVideo)
async def create_video(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_user)
):
    return await save_video(
        user,
        file,
        title,
        description,
    )


@video_router.post("/{video_pk}", status_code=201)
async def add_like(video_pk: int, user: User = Depends(get_user)):
    _video = await Video.objects.select_related("like_user").get(pk=video_pk)
    _user= await User.objects.get(id=user.id)
    if _user in _video.like_user:
        _video.likes -= 1
        await _video.like_user.remove(_user)
    else:
        _video.likes += 1
        await _video.like_user.add(_user)
    await _video.update()



@video_router.get("/user/{user_name}", response_model=List[GetListVideo])
async def get_user_video(user_name: str):
    video_list = await Video.objects.filter(user__username=user_name).all()
    return video_list


@video_router.get("/video-list", response_model=List[GetListVideo])
async def get_video_list():
    return await Video.objects.all()


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def play_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})


@video_router.get("/video/{video_pk}")
async def play_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers
    })
    return response
