from functools import wraps

import jwt
from fastapi import HTTPException, status, Request

from app.dao.user.user_dao import UserDAO
from app.utils import constant

SECRET_KEY = constant.secrets_key

user_dao = UserDAO()


def login_required(required_roles=None, flag=None):
    if required_roles is None:
        required_roles = []

    def decorator(route_function):
        @wraps(route_function)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.headers.get('Authorization')
            if not token and not flag:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Token missing")

            try:
                if token:
                    decoded_data = jwt.decode(token, SECRET_KEY,
                                              algorithms=["HS256"])
                    user_email = decoded_data.get('email')
                    user_role = decoded_data.get('role')

                    if user_role not in required_roles:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this action")

                    if not user_email or not user_role:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token missing")

                user_info = user_dao.get_user_by_email_dao(user_email)

                if not user_info:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid user")

                data = {"user_db_data": user_info, "headers": request}

            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Token has expired")

            except jwt.DecodeError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid token")

            return await route_function(data, *args, **kwargs)

        return wrapper

    return decorator
