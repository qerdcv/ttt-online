import pytest
from dataclasses import asdict
from aiohttp.test_utils import TestClient

from src.models.game import Game


async def test_correct(client: TestClient, game_object: Game):
    response = await client.get(f'/api/games/{game_object.id}')
    assert response.status == 200
    data = await response.json()
    assert data == asdict(game_object)


async def test_game_not_found(client: TestClient, game_object: Game):
    response = await client.get(f'/api/games/{game_object.id + 1}')
    assert response.status == 404
    data = await response.json()
    assert data['message'] == 'game not found'


@pytest.mark.parametrize('_id', [
    'test_room_id',
    'test_room_id_12345',
    '12345test_room_id_12345'
])
async def test_uncorrect_gid(_id, client: TestClient):
    response = await client.get(f'/api/games/{_id}')
    assert response.status == 404
