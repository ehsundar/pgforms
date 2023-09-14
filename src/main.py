from fastapi import FastAPI

from src.internal.crypto.jwt import JsonWebToken
from src.internal.crypto.password import Password
from src.users.router import router as users_router

JsonWebToken.load_keys("./.secret")
Password.load_salt("./.secret")

app = FastAPI(title="pgforms")

app.include_router(router=users_router)
