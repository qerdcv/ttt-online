import math
import random
import typing as t
from enum import Enum
from dataclasses import dataclass, asdict

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
class Player:
    id: t.Optional[int] = None,
    username: t.Optional[str] = None,
    mark: t.Optional[chr] = None


@dataclass
class Game:
    id: int
    owner: Player
    step_count: int
    field: t.Union[str, t.List[chr]]
    current_state: str
    opponent: t.Optional[Player] = None
    current_player: t.Optional[Player] = None
    winner: t.Optional[Player] = None
    player_prefixes = {'owner', 'opponent', 'current_player', 'winner'}

    def _is_win(self) -> bool:
        field = [colum for line in self.field for colum in line]
        for condition in WIN_CONDITIONS:
            if all(field[cell_idx] == self._current_mark() for cell_idx in condition):
                return True
        return False

    def _invert_player(self):
        if self.current_player.id == self.owner.id:
            self.current_player = self.opponent
        else:
            self.current_player = self.owner

    def _current_mark(self) -> chr:
        if self.current_player.id == self.owner.id:
            return self.owner.mark
        return self.opponent.mark

    def set_opponent(self, opponent: User):
        self.opponent = Player(
            id=opponent.id,
            username=opponent.username,
            mark='0'
        )
        self.current_player = random.choice(
            [self.owner, self.opponent]
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
            self.winner = self.current_player
            self.current_state = State.DONE.value
            return
        self._invert_player()
        if self.step_count == field_size:
            self.current_state = State.DONE.value

    @classmethod
    def from_dict(cls, data: dict):
        owner_id = data['owner_id']
        for _, prefix in enumerate(cls.player_prefixes):
            id_ = data.pop(f'{prefix}_id')
            username = data.pop(f'{prefix}_name')
            mark = 'X' if id_ == owner_id else '0'
            if id_ is None:
                mark = None
            data[prefix] = Player(id=id_, username=username, mark=mark)
        return cls(**data)

    def to_dict(self) -> dict:
        res = asdict(self)
        for prefix in self.player_prefixes:
            if not res[prefix]['id']:
                res[prefix] = None
        return res
