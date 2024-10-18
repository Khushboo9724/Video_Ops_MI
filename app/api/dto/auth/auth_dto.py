from pydantic import BaseModel


class LoginDto(BaseModel):
    user_email: str
    password: str


class AccessTokenDto(BaseModel):
    refresh_token: str