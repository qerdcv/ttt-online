import math
import random
import typing as t
from enum import Enum
from dataclasses import dataclass

from schematics.models import Model
from schematics.types import IntType, ListType

from src.middlewares import User
from src.errors.game import CellOccupied


WIN_CONDITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class State(Enum):
    PENDING = 'pending'
    IN_GAME = 'in_game'
    DONE = 'done'


class Step(Model):
    coords = ListType(
        IntType(min_value=0, max_value=2),
        min_size=2,
        max_size=2
    )


@dataclass
class Game:
    id: int
    owner_id: int
    opponent_id: t.Optional[int]
    current_player_id: t.Optional[int]
    step_count: int
    winner_id: t.Optional[int]
    field: t.Union[str, t.List[chr]]
    current_state: str
    owner_mark: chr = 'X'
    opponent_mark: chr = '0'

    def _is_win(self) -> bool:
        field = [colum for line in self.field for colum in line]
        for condition in WIN_CONDITIONS:
            if all(field[cell_idx] == self._current_mark() for cell_idx in condition):
                return True
        return False

    def _invert_player(self):
        if self.current_player_id == self.owner_id:
            self.current_player_id = self.opponent_id
        else:
            self.current_player_id = self.owner_id

    def _current_mark(self) -> chr:
        if self.current_player_id == self.owner_id:
            return self.owner_mark
        return self.opponent_mark

    def set_opponent(self, opponent: User):
        self.opponent_id = opponent.id
        self.current_player_id = random.choice(
            [self.owner_id, self.opponent_id]
        )
        self.current_state = State.IN_GAME.value

    def update(self, coords: t.List[int]):
        row, col = coords
        if self.field[row][col]:
            raise CellOccupied
        field_size = len(self.field) ** 2
        self.field[row][col] = self._current_mark()
        self.step_count += 1
        if self.step_count >= math.ceil(field_size / 2) and self._is_win():
            self.winner_id = self.current_player_id
            self.current_state = State.DONE.value
            return
        self._invert_player()
        if self.step_count == field_size:
            self.current_state = State.DONE.value

    def to_json(self):
        return self.__dict__
