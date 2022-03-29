import jwt
from cryptography.fernet import Fernet

from src.settings import SECRET


FERNET = Fernet(SECRET)


def encrypt(message: str) -> str:
    return FERNET.encrypt(message.encode()).decode('utf-8')


def decrypt(message: str) -> str:
    return FERNET.decrypt(message.encode('utf-8')).decode()


def encrypt_jwt(**kwargs) -> str:
    return jwt.encode(kwargs, SECRET, algorithm='HS256')


def decode_jwt(jwt_token: str) -> dict:
    return jwt.decode(jwt_token, SECRET, algorithms='HS256')


def is_same_messages(hash_message: str, message: str) -> bool:
    return decrypt(hash_message) == message
