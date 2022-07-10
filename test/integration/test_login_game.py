import typing as t

import pytest
from aiohttp.test_utils import TestClient

from src.models.user import User
from src.models.game import Game, State


async def test_success(client: TestClient, logged_user_opponent: User, game_object: Game):
    response = await client.patch(f'/api/games/{game_object.id}/login')
    assert response.status == 200
    data = await response.json()
    assert data['opponent_id'] == logged_user_opponent.id
    assert data['current_state'] == State.IN_GAME.value


@pytest.mark.parametrize('state', [
    State.IN_GAME.value,
    State.DONE.value
])
async def test_invalid_state(state: str, client: TestClient,
                             update_game: t.Callable[[Game], t.Awaitable[None]],
                             game_object: Game, logged_user):
    game_object.current_state = state
    await update_game(game_object)
    response = await client.patch(f'/api/games/{game_object.id}/login')
    assert response.status == 400
    data = await response.json()
    assert data['message'] == 'invalid state'


async def test_game_not_found(client: TestClient, game_object: Game, logged_user: User):
    response = await client.patch(f'/api/games/{game_object.id + 1}/login')
    assert response.status == 404
    data = await response.json()
    assert data['message'] == 'game not found'


@pytest.mark.parametrize('_id', [
    'test_room_id',
    'test_room_id_12345',
    '12345test_room_id_12345'
])
async def test_uncorrect_gid(_id, client: TestClient):
    response = await client.patch(f'/api/games/{_id}/login')
    assert response.status == 404


async def test_unauth(client: TestClient, game_object: Game):
    response = await client.patch(
        f'/api/games/{game_object.id}/login'
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'


async def test_user_in_game(client: TestClient, logged_user: User, game_object: Game):
    response = await client.patch(f'/api/games/{game_object.id}/login')
    assert response.status == 409
    data = await response.json()
    assert data['message'] == 'user already in game'
