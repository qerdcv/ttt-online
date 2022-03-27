import typing as t
from dataclasses import dataclass, asdict


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
    next_state: str
