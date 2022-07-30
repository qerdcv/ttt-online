import typing as t

import pytest
from aiohttp.test_utils import TestClient

from src.models.game import Game, State
from src.models.user import User


COORDS = (0, 0)


@pytest.mark.parametrize(
    'first_coord, coords_list, is_win',
    [
        (
            (0, 0),
            (
                (1, 0),
                (0, 1),
                (1, 1),
                (0, 2)
            ),
            True
        ),  # Horizontal victory
        (
            (0, 0),
            (
                (0, 1),
                (1, 0),
                (1, 1),
                (2, 0)
            ),
            True
        ),  # Vertical victory
        (
            (0, 0),
            (
                (0, 1),
                (1, 1),
                (1, 0),
                (2, 2)
            ),
            True
        ),  # Diagonal victory
        (
            (2, 2),
            (
                (0, 1),
                (1, 1),
                (1, 0),
                (0, 0)
            ),
            True
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
            False
        ),  # Draw
    ]
)
async def test_successes(first_coord: t.Tuple[int], coords_list: t.Tuple[t.Tuple[int]], is_win: bool,
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
        if is_win and idx == len(coords_list) - 1:
            expected_winner_id = game_with_opponent.current_player.id
        response = await client.patch(
            f'/api/games/{game_with_opponent.id}',
            json={'coords': coords}
        )
        await client.get('/api/logout')
    assert response.status == 200
    data = await response.json()
    if is_win:
        assert data['message']['winner']['id'] == expected_winner_id
    else:
        assert data['message']['winner'] is None


async def test_unauth(client: TestClient, game_with_opponent: Game):
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}'
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'


@pytest.mark.parametrize(
    'coords, expected_error',
    [
        ((-1, -1), ('Int value should be greater than or equal to 0.', ) * 2),
        ((-1, 3), ('Int value should be greater than or equal to 0.', 'Int value should be less than or equal to 2.')),
        ((3, -1), ('Int value should be less than or equal to 2.', 'Int value should be greater than or equal to 0.')),
        ((3, 3), ('Int value should be less than or equal to 2.', ) * 2)
    ]
)
async def test_step_valid(client: TestClient, logged_user: User, game_with_opponent: Game,
                          coords: t.Tuple[int], expected_error: t.Tuple[str]):
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': coords}
    )
    assert response.status == 400
    data = await response.json()
    row_msg, = data['coords'].get('0')
    col_msg, = data['coords'].get('1')
    expected_row_error, expected_col_error = expected_error
    assert row_msg == expected_row_error
    assert col_msg == expected_col_error


async def test_game_not_found(client: TestClient, logged_user: User, game_with_opponent: Game):
    response = await client.patch(
        f'/api/games/{game_with_opponent.id + 1}',
        json={'coords': COORDS}
    )
    assert response.status == 404
    data = await response.json()
    assert data['message'] == 'game not found'


@pytest.mark.parametrize('state', [
    State.PENDING.value,
    State.DONE.value
])
async def test_invalid_state(state: str, client: TestClient,
                             login_user: t.Callable[[User], t.Awaitable[User]],
                             test_user: User, game_with_opponent: Game,
                             update_game: t.Callable[[Game], t.Awaitable[None]]):
    await login_user(test_user)
    game_with_opponent.current_state = state
    await update_game(game_with_opponent)
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': COORDS}
    )
    assert response.status == 400
    data = await response.json()
    assert data['message'] == 'invalid state'


async def test_not_your_turn(client: TestClient, login_user: t.Callable[[User], t.Awaitable[User]],
                             test_user: User, test_opponent: User, game_with_opponent: Game):
    if test_user.id != game_with_opponent.current_player.id:
        await login_user(test_user)
    else:
        await login_user(test_opponent)
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': COORDS}
    )
    assert response.status == 403
    data = await response.json()
    assert data['message'] == 'not your turn'


async def test_cell_occupied(client: TestClient, login_user: t.Callable[[User], t.Awaitable[User]],
                             test_user: User, test_opponent: User, game_with_opponent: Game):
    if test_user.id == game_with_opponent.current_player.id:
        await login_user(test_user)
    else:
        await login_user(test_opponent)
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': COORDS}
    )
    await client.get('/api/logout')
    data = await response.json()
    if test_user.id == data['message']['current_player']['id']:
        await login_user(test_user)
    else:
        await login_user(test_opponent)
    response = await client.patch(
        f'/api/games/{game_with_opponent.id}',
        json={'coords': COORDS}
    )
    assert response.status == 409
    data = await response.json()
    assert data['message'] == 'cell is already occupied'
