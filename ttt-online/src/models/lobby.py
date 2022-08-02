import typing as t
from asyncio import Queue

from src.models.game import Game


class Lobby:
    obj = None
    __lobby: t.Dict[int, t.List[Queue]] = {}

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj

    def join(self, game_id: int) -> Queue:
        if game_id not in self.__lobby:
            self.__lobby[game_id] = []
        queue = Queue()
        self.__lobby[game_id].append(queue)
        return queue

    def leave(self, game_id: int, queue: Queue):
        if game_id not in self.__lobby:
            return

        self.__lobby[game_id].remove(queue)

        if not self.__lobby[game_id]:
            del self.__lobby[game_id]

    async def update(self, game_id: int, game: Game):
        if game_id not in self.__lobby:
            return

        for player in self.__lobby[game_id]:
            await player.put(game)
