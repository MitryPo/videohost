from typing import List

from fastapi import APIRouter, File, Form, UploadFile, Depends
from starlette import responses
from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from user.auth import current_active_user
from video.models import User, Video
from video.schemas import GetListVideo
from video.services import open_file, save_video

video_router = APIRouter(tags=["video"])
templates = Jinja2Templates(directory="templates")


@video_router.post('/')
async def create_video(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(current_active_user)
):
    return await save_video(
        user,
        file,
        title,
        description,
    )


# @video_router.get("/video/{video_pk}")
# async def get_video(video_pk:int):
#     file = await Video.objects.select_related('user').get(pk=video_pk)
#     open_file = open(file.dict().get('file'), mode='rb')
#     return StreamingResponse(open_file, media_type="video/mp4")


@video_router.get("/user/{user_pk}", response_model=List[GetListVideo])
async def get_user_video(user_pk: str):
    video_list = await Video.objects.filter(user=user_pk).all()
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
