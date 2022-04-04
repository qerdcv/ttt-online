import pytest
from aiohttp.test_utils import TestClient

from src.db import get_user, update_game
from src.models.user import User
from src.models.game import Game, State


async def test_correct(client: TestClient, login_test_user,
                       test_user: User, game_object: Game):
    response = await client.patch(f'/api/games/{game_object.id}/login')
    assert response.status == 200
    data = await response.json()
    stored_test_user = await get_user(client.app['pool'], test_user)
    assert data['opponent_id'] == stored_test_user.id
    assert data['current_player_id'] == stored_test_user.id
    assert data['current_state'] == State.IN_GAME.value


@pytest.mark.parametrize('state', [
    State.IN_GAME.value,
    State.DONE.value
])
async def test_invalid_state(state: str, client: TestClient,
                             game_object: Game, login_test_user):
    game_object.current_state = state
    await update_game(client.app['pool'], game_object)
    response = await client.patch(f'/api/games/{game_object.id}/login')
    assert response.status == 400
    data = await response.json()
    assert data['message'] == 'invalid state'


async def test_game_not_found(client: TestClient, game_object: Game, login_test_user):
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


async def test_unauth(client: TestClient, test_user: User, game_object: Game):
    response = await client.patch(
        f'/api/games/{game_object.id}/login',
        json={}
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'
