from typing import Annotated

import pydantic
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.crypto.jwt import JsonWebToken
from src.internal.crypto.password import Password
from src.internal.storage import storage
from src.internal.storage.entities.users.models import User
from src.internal.storage.entities.users.users import AsyncQuerier as UsersQuerier
from main import app


class SignupRequest(BaseModel):
    username: str
    password: str
    email: pydantic.EmailStr
    name: str


class SignupResponse(BaseModel):
    jwt: str
    user: User


@app.post("/users/signup", response_model=SignupResponse)
async def signup(
        db: Annotated[AsyncSession, Depends(storage.get_db)],
        jwt: Annotated[JsonWebToken, Depends(JsonWebToken)],
        password: Annotated[Password, Depends(Password)],
        body: SignupRequest,
):
    conn = await db.connection()

    masked_password = password.mask(body.password)

    try:
        users_querier = UsersQuerier(conn)
        user = await users_querier.create_user(
            username=body.username,
            password=masked_password,
            email=body.email,
            name=body.name,
        )
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Username already exists") from exc

    session = await users_querier.create_session(username=user.username)

    token = jwt.generate(user, session)

    await conn.commit()

    user.password = ""

    return SignupResponse(
        user=user,
        jwt=token,
    )
