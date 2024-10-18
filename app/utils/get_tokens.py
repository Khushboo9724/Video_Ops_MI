from datetime import datetime, timedelta

import jwt

from app import constant
from app.custom_enum.static_enum import StaticVariables

SECRET_KEY = constant.secrets_key


def generate_tokens(email, role_name):
    access_token_payload = {
        'exp': datetime.utcnow() + timedelta(days=0,
                                             minutes=int(
                                                 StaticVariables.ACCESS_TOKEN_EXPIRE_MINUTES),
                                             seconds=0),
        'iat': datetime.utcnow(),
        'email': email,
        'role': role_name
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY,
                              algorithm=StaticVariables.ALGORITHM)

    refresh_token_payload = {
        'iat': datetime.utcnow(),
        'email': email,
        'role': role_name
    }
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY,
                               algorithm=StaticVariables.ALGORITHM)

    return {'Access_Token': access_token, 'Refresh_Token': refresh_token}
