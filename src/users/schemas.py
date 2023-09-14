import pydantic
from pydantic import BaseModel

from src.internal.storage.entities.users.models import User


class SignupRequest(BaseModel):
    username: str
    password: str
    email: pydantic.EmailStr
    name: str


class SignupResponse(BaseModel):
    jwt: str
    user: User
