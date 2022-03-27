import jwt
from cryptography.fernet import Fernet

from src.settings import SECRET


FERNET = Fernet(SECRET)


def encrypt_password(msg: str) -> str:
    enc_message = FERNET.encrypt(msg.encode())
    return enc_message.decode('utf-8')


def decrypt_password(msg: str) -> str:
    msg = msg.encode('utf-8')
    dec_message = FERNET.decrypt(msg).decode()
    return dec_message


def encrypt_jwt(**kwargs) -> str:
    return jwt.encode(kwargs, 'some_key', algorithm='HS256')


def decode_jwt(jwt_token: str) -> dict:
    return jwt.decode(jwt_token, 'some_key', algorithms='HS256')
