from enum import Enum


class StaticVariables(str, Enum):
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    ADMIN_ROLE_ENUM = "admin"
    USER_ROLE_ENUM = "user"
