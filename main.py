from typing import Annotated

import uvicorn
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.app.app import app
from src.internal.crypto.jwt import JsonWebToken
from src.internal.crypto import Password
from src.internal.storage import storage
from src.internal.storage.entities.users.models import User
from src.internal.storage.entities import AsyncQuerier as UsersQuerier


@app.get("/users/{username}", response_model=User)
async def get_user(db: Annotated[AsyncSession, Depends(storage.get_db)], username: str):
    conn = await db.connection()

    querier = UsersQuerier(conn)
    user = await querier.get_user(username=username)

    await db.commit()

    return user


if __name__ == "__main__":
    JsonWebToken.load_keys("./.secret")
    Password.load_salt("./.secret")

    uvicorn.run(app, host="0.0.0.0", port=8000)
