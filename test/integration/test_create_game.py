from aiohttp.test_utils import TestClient

from src.models.user import User
from src.db import get_user


async def test_correct(client: TestClient, test_user: User, login_test_user):
    response = await client.post(
        '/api/games',
        json={}
    )
    assert response.status == 201
    data = await response.json()
    stored_test_user = await get_user(client.app['pool'], test_user)
    assert data['owner_id'] == stored_test_user.id


async def test_unauth(client: TestClient, test_user: User):
    response = await client.post(
        '/api/games',
        json={}
    )
    assert response.status == 401
    data = await response.json()
    assert data['message'] == 'unauthorized'
