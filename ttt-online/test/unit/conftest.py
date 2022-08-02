import pytest

from src.models.user import User
from src.models.game import Game, State, Player


@pytest.fixture
def user_object() -> User:
    return User(
        {
            'username': 'test_user',
            'password': '12345'
        }
    )


@pytest.fixture
def user_opponent_object(user_object: User) -> User:
    return User(
        {
            'username': user_object.username + '_opponent',
            'password': str(user_object.password)
        }
    )


@pytest.fixture
def fake_game_object() -> Game:
    return Game(
        id=1,
        owner=Player(
            id=1,
            name='test',
            mark='X'
        ),
        opponent=None,
        current_player=None,
        step_count=0,
        winner=None,
        field=[
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ],
        current_state=State.PENDING.value
    )


@pytest.fixture
def fake_game_with_opponent(fake_game_object: Game, user_opponent_object: User) -> Game:
    user_opponent_object.id = fake_game_object.owner.id + 1
    fake_game_object.set_opponent(user_opponent_object)
    return fake_game_object
