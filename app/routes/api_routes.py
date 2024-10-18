from fastapi import APIRouter

from app.api.controller.admin import admin_controller
from app.api.controller.auth import auth_controller
from app.api.controller.user import user_controller
from app.api.controller.video import video_controller
from app.api.controller.health_check import health_check_controller


router = APIRouter()
router.include_router(user_controller.user_router)

router.include_router(admin_controller.admin_router)
router.include_router(auth_controller.login_router)
router.include_router(video_controller.video_router)
router.include_router(health_check_controller.health_check_router)
