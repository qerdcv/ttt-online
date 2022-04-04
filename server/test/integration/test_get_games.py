import math
import typing as t

import pytest
from aiohttp.test_utils import TestClient

COUNT_GAME = 21


@pytest.mark.parametrize('page, limit, expected_page, expected_limit, expected_count_games', [
    (None, None, 1, 10, 10),
    (None, 10, 1, 10, 10),
    (1, None, 1, 10, 10),
    (0, 10, 1, 10, 10),
    (2, 1, 2, 1, 1),
    (2, 100, 2, 100, 0),
    (1, 1000000, 1, 100, 21),
    (1.9, 1.9, 1, 10, 10),
    ('test', 'test', 1, 10, 10)
])
async def test_correct(page: int, limit: int,
                       expected_page: int, expected_limit: int, expected_count_games: int,
                       client: TestClient,
                       game_factory: t.Callable[[int], t.Awaitable[None]]):
    await game_factory(COUNT_GAME)
    response = await client.get(f'/api/games?page={page}&limit={limit}')
    assert response.status == 200
    data = await response.json()
    assert len(data['games']) == expected_count_games
    assert data['paginator']['page'] == expected_page
    assert data['paginator']['limit'] == expected_limit
    assert data['paginator']['total_games'] == math.ceil(COUNT_GAME / expected_limit)
