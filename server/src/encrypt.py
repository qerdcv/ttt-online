from cryptography.fernet import Fernet


def encrypt(key: str, msg: str) -> str:
    fernet = Fernet(key)
    encMessage = fernet.encrypt(msg.encode())
    return encMessage.decode('utf-8')


def decrypt(key: str, msg: str) -> str:
    fernet = Fernet(key)
    msg = msg.encode('utf-8')
    decMessage = fernet.decrypt(msg).decode()
    return decMessage
