from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.sources.router import router as sources_router
from src.users.crypto.jwt import JsonWebToken
from src.users.router import router as users_router

JsonWebToken.load_keys("./.secret")

app = FastAPI(title="pgforms")

app.include_router(router=users_router)
app.include_router(router=sources_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
