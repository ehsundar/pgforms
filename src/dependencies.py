from typing import Annotated

from authlib.jose.errors import BadSignatureError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src import database
from src.users.crypto.jwt import JsonWebToken
from src.users.queries import AsyncQuerier

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(database.get_db)],
        json_web_token: Annotated[JsonWebToken, Depends(JsonWebToken)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        _, username = json_web_token.validate(token)
        if username is None:
            raise credentials_exception
    except BadSignatureError:
        raise credentials_exception

    conn = await db.connection()

    users_querier = AsyncQuerier(conn)
    user = await users_querier.get_user(username=username)

    if user is None:
        raise credentials_exception
    return user
