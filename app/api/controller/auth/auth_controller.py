from fastapi import APIRouter, Response

from app.config.logger_config import MyLogger
from app.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from app.api.dto.auth.auth_dto import LoginDto, AccessTokenDto
from app.service.auth import auth_service
from app.service.common.common_service import AppServices

logger = MyLogger.get_logger(__name__)

login_router = APIRouter(
    prefix="/auth",
    tags=["Login"],
    responses={404: {"description": "Api Endpoint Not found"}},
)


@login_router.post("/login")
async def user_login(login_dto: LoginDto):

    try:

        response_payload = auth_service.login_service(login_dto)
        response = AppServices.app_response(
            status_code=HttpStatusCodeEnum.OK,
            message="Login Successful",
            success=True,
            data=response_payload
        )
        logger.info(f"Response for login is {response_payload}")
        return response
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)


@login_router.post("/get-refresh-token")
async def get_refresh_token(access_token_dto: AccessTokenDto):
    try:
        response_payload = auth_service.get_refresh_token_service(access_token_dto)
        response = AppServices.app_response(
            status_code=HttpStatusCodeEnum.OK,
            message="Refresh token fetched successfully!",
            success=True,
            data=response_payload
        )
        logger.info(f"Response for new access token is {response_payload}")
        return response
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)
