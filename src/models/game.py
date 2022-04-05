import random
import typing as t
from enum import Enum
from dataclasses import dataclass

from src.middlewares import User


class State(Enum):
    PENDING = 'pending'
    IN_GAME = 'in_game'
    DONE = 'done'


@dataclass
class Game:
    id: int
    owner_id: int
    opponent_id: t.Optional[int]
    current_player_id: t.Optional[int]
    step_count: int
    winner_id: t.Optional[int]
    field: t.Union[str, list]
    current_state: str

    def set_opponent(self, opponent: User):
        self.opponent_id = opponent.id
        self.current_player_id = random.choice(
            [self.owner_id, self.opponent_id]
        )
        self.current_state = State.IN_GAME.value

    def to_json(self):
        return self.__dict__
