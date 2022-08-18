class InvalidDate(Exception):
    def __init__(self, message: str = 'invalid data'):
        self._message = message
        super().__init__(message)

    def to_dict(self) -> dict:
        return {'message': self._message}
