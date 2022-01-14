from cryptography.fernet import Fernet

from src.settings import SECRET


fernet = Fernet(SECRET)


def encrypt(msg: str) -> str:
    encMessage = fernet.encrypt(msg.encode())
    return encMessage.decode('utf-8')


def decrypt(msg: str) -> str:
    msg = msg.encode('utf-8')
    decMessage = fernet.decrypt(msg).decode()
    return decMessage
