class UsernameError(Exception):
    def __init__(self, message="user don't exists"):
        self.message = message
        super().__init__(self.message)

    def to_primitive(self):
        return {'message': self.message}


class UserPasswordError(Exception):
    def __init__(self, message="wrong password"):
        self.message = message
        super().__init__(self.message)

    def to_primitive(self):
        return {'message': self.message}
