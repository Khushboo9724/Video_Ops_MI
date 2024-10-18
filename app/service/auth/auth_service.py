import jwt
from datetime import datetime, timedelta

from app import constant
from app.custom_enum.static_enum import StaticVariables

from app.dao.user.user_dao import UserDAO
from app.utils.get_tokens import generate_tokens
from app.utils.password_hash import verify_password

from app.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from app.service.common.common_service import AppServices

SECRET_KEY = constant.secrets_key

def login_service(login_data):
    try:
        user_dao = UserDAO()

        # Get username and password
        login_user_email = login_data.user_email
        login_pass = login_data.password

        user_info = user_dao.get_user_by_email_dao(login_user_email)

        if user_info is None:
            return AppServices.app_response(HttpStatusCodeEnum.NOT_FOUND,
                                            ResponseMessageEnum.USER_NOT_FOUND,
                                            success=False,
                                            data={})
        check_user_password = verify_password(input_password=login_pass,
                                              hashed_password=user_info.password)

        if not check_user_password:
            return AppServices.app_response(HttpStatusCodeEnum.UNAUTHORIZED,
                                            ResponseMessageEnum.LOGIN_FAILED,
                                            success=False,
                                            data={})

        token_data = generate_tokens(user_info.email, user_info.role)
        # Update Role in "token_data" dict
        token_data.update(firstname=user_info.firstname)
        token_data.update(lastname=user_info.lastname)
        token_data.update(email=user_info.email)
        token_data.update(Role=user_info.role)

        return token_data

    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)



def get_refresh_token_service(request_data):
    try:
        # Get refresh token from request data
        refresh_token = request_data.refresh_token
        # Decode the refresh token and verify if the user's email is present
        decoded_data = jwt.decode(jwt=refresh_token,
                                  key=SECRET_KEY,
                                  algorithms=[StaticVariables.ALGORITHM])
        user_email = decoded_data.get('email')

        if not user_email:
            return AppServices.app_response(HttpStatusCodeEnum.NOT_FOUND,
                                            ResponseMessageEnum.USER_NOT_FOUND,
                                            success=False,
                                            data={})
        user_dao = UserDAO()
        user_info = user_dao.get_user_by_email_dao(user_email)

        if user_info is None:
            return AppServices.app_response(HttpStatusCodeEnum.NOT_FOUND,
                                            ResponseMessageEnum.USER_NOT_FOUND,
                                            success=False,
                                            data={})
        # Retrieve the role name associated with a given role ID from the database
        # Extract user information fields, handling missing attributes gracefully
        email = getattr(user_info, 'email', None)
        access_token_payload = {
            'exp': datetime.utcnow() + timedelta(days=0,
                                                 minutes=int(StaticVariables.ACCESS_TOKEN_EXPIRE_MINUTES),
                                                 seconds=0),
            'iat': datetime.utcnow(),
            'user_email': email,
            'user_role': user_info.role
        }

        refresh_token = jwt.encode(access_token_payload,
                                  SECRET_KEY,
                                  algorithm=StaticVariables.ALGORITHM)
        token_data = {'refresh_token': refresh_token}
        return AppServices.app_response(HttpStatusCodeEnum.OK,
                                        ResponseMessageEnum.GET_ACCESS_TOKEN,
                                        success=True,
                                        data=token_data)
    except jwt.DecodeError:
        return AppServices.app_response(HttpStatusCodeEnum.UNAUTHORIZED,
                                        ResponseMessageEnum.INVALID_ACCESS_TOKEN,
                                        success=False,
                                        data={})

    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)