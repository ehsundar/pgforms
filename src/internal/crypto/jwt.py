from datetime import timedelta
from os import path
from typing import Tuple

from authlib.jose import jwt

from src.internal.storage.entities.users.models import User, Session


class JsonWebToken:
    _private_key: str
    _public_key: str

    @classmethod
    def load_keys(cls, directory_path: str):
        with open(path.join(directory_path, "jwtRS256.key"), "r", encoding="utf-8") as f:
            cls._private_key = f.read()

        with open(path.join(directory_path, "jwtRS256.key.pub"), "r", encoding="utf-8") as f:
            cls._public_key = f.read()

    def generate(self, user: User, session: Session) -> str:
        session_jwt = jwt.encode(
            header={"alg": "RS256"},
            payload={
                "iss": "Authlib",
                "sub": user.username,
                "aud": "pgforms",
                "exp": session.issued_at + timedelta(days=7),
                "nbf": session.issued_at,
                "iat": session.issued_at,
                "jti": str(session.id),
            },
            key=self._private_key,
        )

        return str(session_jwt, "utf-8")

    def validate(self, token: str) -> Tuple[str, str]:
        jwt.decode(token, self._public_key)

