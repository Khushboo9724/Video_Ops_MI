from pydantic import BaseModel


class UserDTO(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
