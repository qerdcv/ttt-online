import pytest

from src.models.game import Game
from src.errors.game import CellOccupied


def change_current_mark(owner_id: int, current_player_id: int) -> chr:
    if owner_id == current_player_id:
        return 'X'
    return '0'


COORDS_LIST = [(idx, jdx) for idx in range(2) for jdx in range(3)]


def test_successes(fake_game_with_opponent: Game):
    for coords in COORDS_LIST:
        current_mark = change_current_mark(
            fake_game_with_opponent.owner.id,
            fake_game_with_opponent.current_player.id
        )
        prev_current_player_id = fake_game_with_opponent.current_player.id
        row, col = coords
        fake_game_with_opponent.update([row, col])
        assert fake_game_with_opponent.field[row][col] == current_mark
        assert fake_game_with_opponent.current_player.id != prev_current_player_id


def test_cell_occupied(fake_game_with_opponent: Game):
    for coords in COORDS_LIST:
        fake_game_with_opponent.update(coords)
        with pytest.raises(CellOccupied):
            fake_game_with_opponent.update(coords)
