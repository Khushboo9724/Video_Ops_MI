from app.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from app.dao.user.user_dao import UserDAO
from app.service.common.common_service import AppServices
from app.utils.date_parse_utils import DateParseUtils
from app.utils.password_hash import hash_password
from app.vo.user_vo import UserVO


def user_register(req_data):
    try:
        user_dao = UserDAO()
        user_vo = UserVO()
        user_info = user_dao.get_user_by_email_dao(req_data.email)
        if user_info:
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.BAD_REQUEST,
                message=ResponseMessageEnum.USER_ALREADY_EXIST,
                success=False,
                data={})
        current_datetime = DateParseUtils()

        get_current_epoc_time = current_datetime.get_current_epoch()

        user_vo.firstname = req_data.firstname
        user_vo.lastname = req_data.lastname
        user_vo.email = req_data.email
        user_vo.role = 'user'
        user_vo.password = hash_password(password=req_data.password)
        user_vo.is_deleted = False
        user_vo.created_on = get_current_epoc_time
        user_vo.modified_on = get_current_epoc_time

        insert_user_dao = user_dao.insert_user_dao(user_vo)

        if not insert_user_dao:
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                message=ResponseMessageEnum.INTERNAL_SERVER_ERROR,
                success=False,
                data={})

        return AppServices.app_response(
            status_code=HttpStatusCodeEnum.CREATED,
            message=ResponseMessageEnum.INSERT_DATA,
            success=True,
            data={})
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)
