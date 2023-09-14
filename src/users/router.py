from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.crypto.jwt import JsonWebToken
from src.internal.crypto.password import Password
from src.internal.storage import storage
from src.internal.storage.entities.users.users import AsyncQuerier as UsersQuerier
from src.users.schemas import SignupRequest, SignupResponse

router = APIRouter()


@router.post("/users/signup", response_model=SignupResponse, tags=["users"])
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
