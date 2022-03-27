import random
import typing as t
from dataclasses import dataclass

from src.middlewares import User


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
        self.current_state = 'in_game'
