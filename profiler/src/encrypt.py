from cryptography.fernet import Fernet

from src.config import Config


FERNET = Fernet(Config.secret)


def encrypt(message: str) -> str:
    return FERNET.encrypt(message.encode()).decode('utf-8')


def decrypt(message: str) -> str:
    return FERNET.decrypt(message.encode('utf-8')).decode()


def is_same_messages(hash_message: str, message: str) -> bool:
    return decrypt(hash_message) == message
