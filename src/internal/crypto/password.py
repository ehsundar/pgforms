from hashlib import sha256
from os import path


class Password:
    _salt: str

    @classmethod
    def load_salt(cls, directory_path: str):
        with open(path.join(directory_path, "password_salt.txt"), "r", encoding="utf-8") as f:
            cls._salt = f.read()

    def mask(self, pwd: str) -> str:
        return sha256((self._salt + pwd).encode("utf-8")).hexdigest()

    def validate(self, pwd: str, masked_pwd: str) -> bool:
        return sha256((self._salt + pwd).encode("utf-8")).hexdigest() == masked_pwd
