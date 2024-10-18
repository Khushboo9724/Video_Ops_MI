from fastapi import APIRouter, Response

from app.config.logger_config import MyLogger
from app.api.dto.user.user_dto import  UserDTO
from app.service.common.common_service import AppServices
from app.service.user import user_service

logger = MyLogger.get_logger(__name__)

user_router = APIRouter(
    prefix="/user",
    tags=["Login"],
    responses={404: {"description": "Api Endpoint Not found"}},
)


@user_router.post('/register')
async def user_register(user_dto: UserDTO, response: Response):
    try:
        response_payload = user_service.user_register(req_data=user_dto)
        response.status_code = response_payload.get("status_code")
        return response_payload
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)
