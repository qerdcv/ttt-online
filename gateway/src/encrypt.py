import jwt

from src.config import Config


def encrypt_jwt(**kwargs) -> str:
    return jwt.encode(kwargs, Config.secret, algorithm='HS256')


def decode_jwt(jwt_token: str) -> dict:
    return jwt.decode(jwt_token, Config.secret, algorithms='HS256')
