from src import encrypt, db
from src.models.user import User
from src.errors.user import NotFound, WrongPassword


class Profiler:
    _obj = None
    _user_crud: db.UserCRUD = db.UserCRUD()

    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = super().__new__(cls, *args, **kwargs)
        return cls._obj

    async def login(self, user: User) -> User:
        user.validate()
        stored_user = await self._user_crud.get(user)
        if stored_user is None:
            raise NotFound
        if not encrypt.is_same_messages(stored_user.password, user.password):
            raise WrongPassword
        return stored_user

    async def create(self, user: User):
        user.validate()
        await self._user_crud.create(user)
