from src.models.game import Game, State
from src.models.user import User


def test_successes(fake_game_object: Game, user_opponent_object: User):
    user_opponent_object.id = fake_game_object.owner.id + 1
    fake_game_object.set_opponent(user_opponent_object)
    assert fake_game_object.opponent.id == user_opponent_object.id
    assert fake_game_object.opponent.name == user_opponent_object.username
    assert fake_game_object.current_state == State.IN_GAME.value
