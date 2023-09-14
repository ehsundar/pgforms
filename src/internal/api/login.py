from typing import Annotated

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.app.app import app
from src.internal.crypto.jwt import JsonWebToken
from src.internal.crypto.password import Password
from src.internal.storage.entities.users.models import User
from src.internal.storage.entities.users.users import AsyncQuerier
from src.internal.storage.storage import get_db


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    jwt: str
    user: User


@app.post("/login", response_model=LoginResponse)
async def login(
        db: Annotated[AsyncSession, get_db],
        password: Annotated[Password, Password],
        json_web_token: Annotated[JsonWebToken, JsonWebToken],
        body: LoginRequest,
):
    conn = await db.connection()

    user_querier = AsyncQuerier(conn)

    user = await user_querier.get_user(username=body.username)

    if not password.validate(user.password, body.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    session = await user_querier.create_session(username=user.username)

    jwt = json_web_token.generate(user, session)

    return LoginResponse(user=user, jwt=jwt)
