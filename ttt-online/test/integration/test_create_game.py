from aiohttp.test_utils import TestClient

from src.models.user import User


async def test_success(client: TestClient, logged_user: User):
    response = await client.post(
        '/api/games'
    )
    assert response.status == 201
    data = await response.json()
    assert data['owner_id'] == logged_user.id
    assert data['owner_name'] == logged_user.username


async def test_unauth(client: TestClient):
    response = await client.post(
        '/api/games'
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'
