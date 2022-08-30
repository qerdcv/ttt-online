import typing as t

import pytest
from aiohttp.test_utils import TestClient

from src.models.game import Game
from src.models.user import User


@pytest.mark.parametrize(
    'first_coord, coords_list',
    [
        (
                (0, 0),
                (
                        (1, 0),
                        (0, 1),
                        (1, 1),
                        (0, 2)
                ),
        ),  # Horizontal victory
        (
                (0, 0),
                (
                        (0, 1),
                        (1, 0),
                        (1, 1),
                        (2, 0)
                ),
        ),  # Vertical victory
        (
                (0, 0),
                (
                        (0, 1),
                        (1, 1),
                        (1, 0),
                        (2, 2)
                ),
        ),  # Diagonal victory
        (
                (2, 2),
                (
                        (0, 1),
                        (1, 1),
                        (1, 0),
                        (0, 0)
                ),
        ),  # Reverse diagonal victory
        (
                (0, 0),
                (
                        (0, 1),
                        (0, 2),
                        (1, 1),
                        (2, 1),
                        (2, 0),
                        (2, 2),
                        (1, 2),
                        (1, 0)
                ),
        ),  # Draw
    ]
)
async def test_success(first_coord: t.Tuple[int], coords_list: t.Tuple[t.Tuple[int]],
                       client: TestClient, login_user: t.Callable[[User], t.Awaitable[User]],
                       test_user: User, test_opponent: User, game_with_opponent: Game):
    if test_user.id == game_with_opponent.current_player.id:
        await login_user(test_user)
    else:
        await login_user(test_opponent)
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': first_coord}
    )
    await client.get('/api/logout')
    for idx, coords in enumerate(coords_list):
        game = await response.json()
        if test_user.id == game['message']['current_player']['id']:
            await login_user(test_user)
        else:
            await login_user(test_opponent)
        response = await client.patch(
            f'/api/games/{game_with_opponent.id}',
            json={'coords': coords}
        )
        await client.get('/api/logout')
    await login_user(test_user)
    response = await client.get(
        f'/api/games/{game_with_opponent.id}/history'
    )
    assert response.status == 200
    data = await response.json()
    assert len(data) == len(coords_list) + 2


async def test_unauth(client: TestClient, game_object: Game):
    response = await client.get(
        f'/api/games/{game_object.id}/history'
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'


async def test_game_not_found(client: TestClient, logged_user: User, game_with_opponent: Game):
    response = await client.get(f'/api/games/{game_with_opponent.id + 1}/history')
    assert response.status == 404
    data = await response.json()
    assert data['message'] == 'game not found'
