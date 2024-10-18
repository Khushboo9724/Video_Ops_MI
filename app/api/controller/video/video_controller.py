import os

from fastapi import APIRouter, UploadFile, File, Request, Response
from starlette.responses import FileResponse

from app.custom_enum.http_enum import HttpStatusCodeEnum
from app.custom_enum.static_enum import StaticVariables
from app.custom_enum.video_enum import VideoResponseMsgEnum
from app.service.common.common_service import AppServices
from app.service.video_ops.video_service import VideoService
from app.utils.authentication_check import login_required

video_router = APIRouter(
    prefix="/video",
    tags=["Video"],
    responses={404: {"description": "Api Endpoint Not found"}},
)


@video_router.post("/upload")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
async def upload_video(request: Request, response: Response, file: UploadFile = File(...)):
    try:
        video_service = VideoService()
        response_dict = await video_service.upload_and_convert(file)
        response_data = AppServices.app_response(
            status_code=HttpStatusCodeEnum.OK,
            success=True,
            message=VideoResponseMsgEnum.UPLOAD_SUCCESS_MSG,
            data=response_dict
        )
        response.status_code = HttpStatusCodeEnum.OK
        return response_data
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)


@video_router.get("/download/{video_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM, StaticVariables.USER_ROLE_ENUM])
async def download_video(request: Request, video_id: int, response: Response):
    try:
        video_service = VideoService()

        if video_service.is_video_blocked(video_id):
            response.status_code = HttpStatusCodeEnum.FORBIDDEN
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.FORBIDDEN,
                success=False,
                message=VideoResponseMsgEnum.VIDEO_BLOCKED_DOWNLOAD_ERROR,
                data={}
            )

        video_path = video_service.get_video_path_by_id(video_id)

        if not video_path:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.NOT_FOUND,
                success=False,
                message=VideoResponseMsgEnum.VIDEO_NOT_FOUND_MSG,
                data={}
            )

        headers = {
            'Content-Disposition': f'attachment; filename="{os.path.basename(video_path)}"'
        }

        return FileResponse(video_path, media_type="video/mp4",
                            headers=headers)

    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)

@video_router.get("/search/")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
async def search_video(request: Request, search_keyword: str, response: Response):
    try:
        video_service = VideoService()

        video_list = video_service.search_videos_by_metadata(search_keyword)

        if not video_list:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.NOT_FOUND,
                success=False,
                message=VideoResponseMsgEnum.VIDEO_NOT_FOUND_MSG,
                data={}
            )
        response.status_code = HttpStatusCodeEnum.OK
        return AppServices.app_response(
            status_code=HttpStatusCodeEnum.OK,
            success=True,
            message=VideoResponseMsgEnum.VIDEO_SEARCH_SUCCESS_MSG,
            data=video_list
        )
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)

@video_router.post("/block/{video_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM, StaticVariables.USER_ROLE_ENUM])
async def block_video(request: Request, video_id: int, response: Response):
    try:
        video_service = VideoService()
        blocked = video_service.block_video(video_id)

        if blocked:
            response.status_code = HttpStatusCodeEnum.OK
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.OK,
                success=True,
                message=VideoResponseMsgEnum.VIDEO_BLOCKED_MSG,
                data={"video_id": video_id}
            )
        else:
            response.status_code = HttpStatusCodeEnum.NOT_FOUND
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.NOT_FOUND,
                success=False,
                message=VideoResponseMsgEnum.VIDEO_NOT_FOUND_MSG,
                data={}
            )
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)

@video_router.post("/unblock/{video_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM, StaticVariables.USER_ROLE_ENUM])
async def unblock_video(request: Request, video_id: int, response: Response):
    try:
        video_service = VideoService()
        unblocked = video_service.unblock_video(video_id)

        if unblocked:
            response.status_code=HttpStatusCodeEnum.OK
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.OK,
                success=True,
                message=VideoResponseMsgEnum.VIDEO_UNBLOCKED_MSG,
                data={"video_id": video_id}
            )
        else:
            response.status_code=HttpStatusCodeEnum.NOT_FOUND
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.NOT_FOUND,
                success=False,
                message=VideoResponseMsgEnum.VIDEO_NOT_FOUND_MSG,
                data={}
            )
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)
