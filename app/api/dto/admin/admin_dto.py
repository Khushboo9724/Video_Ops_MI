from pydantic import BaseModel


class AdminDTO(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

