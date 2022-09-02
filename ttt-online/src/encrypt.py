from hashlib import pbkdf2_hmac

import jwt

from src.settings import SECRET


COUNT_ITERATION = 100_000


def encrypt_password(password: str) -> str:
    return pbkdf2_hmac(
        'sha256', password.encode(), SECRET.encode() * 2, COUNT_ITERATION
    ).hex()


def encrypt_jwt(**kwargs) -> str:
    return jwt.encode(kwargs, SECRET, algorithm='HS256')


def decode_jwt(jwt_token: str) -> dict:
    return jwt.decode(jwt_token, SECRET, algorithms='HS256')
