from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user
from src.users.crypto.jwt import JsonWebToken
from src import database
from src.users.models import User
from src.users.queries import AsyncQuerier
from src.users.schemas import SignupRequest, SignupResponse, LoginRequest, LoginResponse, Token

router = APIRouter(prefix="/users", tags=["users"])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup", response_model=SignupResponse)
async def signup(
        db: Annotated[AsyncSession, Depends(database.get_db)],
        jwt: Annotated[JsonWebToken, Depends(JsonWebToken)],
        body: SignupRequest,
):
    conn = await db.connection()

    masked_password = password_context.hash(body.password)

    try:
        users_querier = AsyncQuerier(conn)
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


@router.post("/token", response_model=Token)
async def login_for_access_token(
        db: Annotated[AsyncSession, Depends(get_db)],
        json_web_token: Annotated[JsonWebToken, Depends(JsonWebToken)],
        body: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    conn = await db.connection()

    user_querier = AsyncQuerier(conn)

    user = await user_querier.get_user(username=body.username)

    if not user or not password_context.verify(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session = await user_querier.create_session(username=user.username)

    jwt = json_web_token.generate(user, session)

    return {"access_token": jwt, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    current_user.password = ""
    return current_user
