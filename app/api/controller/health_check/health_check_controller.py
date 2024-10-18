from fastapi import APIRouter

from app.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from app.service.common.common_service import AppServices

health_check_router = APIRouter()




@health_check_router.get('/health-check')
def api_health_check_api():
    try:
        response_payload = AppServices.app_response(
            HttpStatusCodeEnum.OK.value,
            ResponseMessageEnum.HEALTH_CHECK_API_WORKING_SUCCESS_MESSAGE.value,
            True)
        return response_payload
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)