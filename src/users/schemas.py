import pydantic
from pydantic import BaseModel

from src.users.models import User


class SignupRequest(BaseModel):
    username: str
    password: str
    email: pydantic.EmailStr
    name: str


class SignupResponse(BaseModel):
    jwt: str
    user: User


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    jwt: str
    user: User


class Token(BaseModel):
    access_token: str
    token_type: str
