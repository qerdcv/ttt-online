class NotFound(Exception):
    def __init__(self, message: str = 'user don\'t exists'):
        self._message = message
        super().__init__(message)

    def to_dict(self) -> dict:
        return {'message': self._message}


class WrongPassword(Exception):
    def __init__(self, message: str = 'wrong password'):
        self._message = message
        super().__init__(message)

    def to_dict(self) -> dict:
        return {'message': self._message}
