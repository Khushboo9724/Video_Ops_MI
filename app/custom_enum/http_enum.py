from enum import Enum


class HttpStatusCodeEnum(int, Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class ResponseMessageEnum(str, Enum):
    # Common Messages
    HEALTH_CHECK_API_WORKING_SUCCESS_MESSAGE = "Health Check API working success."
    USER_NOT_FOUND = "User not found"
    INTERNAL_SERVER_ERROR = "Oops! Something went wrong"
    LOGIN_FAILED = "Invalid credentials, please try again"
    GET_ACCESS_TOKEN = "New access token obtained successfully"
    INVALID_ACCESS_TOKEN = "Oops! Invalid access token"
    USER_ALREADY_EXIST = "User already exists"
    INSERT_DATA = "Data Inserted Successfully"
