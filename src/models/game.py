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

    def _game_loop(self, field: t.List[str]):
        for condition in WIN_CONDITIONS:
            if all(field[cell_id] == self._current_mark() for cell_id in condition):
                self.winner_id = self.current_player_id
                self.current_state = State.DONE.value
                break

    def _check_win(self):
        one_line_field = [colum for line in self.field for colum in line]
        if one_line_field.count('') == 0:
            self.current_state = State.DONE.value
        else:
            self._game_loop(one_line_field)

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
        self.owner_mark, self.opponent_mark = 'X', '0'
        self.current_state = State.IN_GAME.value

    def update(self, coords: t.List[int]):
        if self.field[coords[0]][coords[1]] not in ('X', '0'):
            field_size = len(self.field) ** 2
            self.field[coords[0]][coords[1]] = self._current_mark()
            self.step_count += 1
            if self.step_count >= math.ceil(field_size / 2):
                self._check_win()
            self._invert_player()
            if self.step_count > field_size:
                self.current_state = State.DONE.value
        else:
            raise CellOccupied

    def to_json(self):
        return self.__dict__
