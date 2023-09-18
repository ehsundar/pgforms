from fastapi import FastAPI

from src.sources.router import router as sources_router
from src.users.crypto.jwt import JsonWebToken
from src.users.router import router as users_router

JsonWebToken.load_keys("./.secret")

app = FastAPI(title="pgforms")

app.include_router(router=users_router)
app.include_router(router=sources_router)
