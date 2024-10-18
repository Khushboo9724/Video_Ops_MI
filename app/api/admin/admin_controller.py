from fastapi import APIRouter, Response

from app.config.logger_config import MyLogger
from app.api.dto.admin.admin_dto import AdminDTO
from app.service.admin import admin_service
from app.service.common.common_service import AppServices

logger = MyLogger.get_logger(__name__)

admin_router = APIRouter(
    prefix="/admin",
    tags=["Login"],
    responses={404: {"description": "Api Endpoint Not found"}},
)


@admin_router.post('/register')
async def admin_register(admin_dto: AdminDTO):
    try:
        response_payload = admin_service.admin_register(req_data=admin_dto)
        return response_payload
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)
