import pytest
from aiohttp.test_utils import TestClient

from src.models.user import User


async def test_correct(client: TestClient, user_object: User):
    response = await client.post(
        '/api/registration',
        json={
            'username': user_object.username,
            'password': user_object.password
        }
    )
    assert response.status == 201
    data = await response.json()
    assert data['message'] == 'OK'


async def test_user_already_exists(client: TestClient, test_user: User):
    response = await client.post(
        '/api/registration',
        json={
            'username': test_user.username,
            'password': test_user.password
        }
    )
    assert response.status == 409
    data = await response.json()
    assert data['message'] == 'user with that name already exists'


# TODO: refactor for max size password or username
@pytest.mark.parametrize('username, password', [
    ('te', '12'),
    ('test_username', '12'),
    ('te', '12345')
])
async def test_validation_error(username: str, password: str, client: TestClient):
    response = await client.post(
        '/api/registration',
        json={
            'username': username,
            'password': password
        }
    )
    assert response.status == 400
    data = await response.json()
    if data.get('username', False) and not data.get('password', False):
        assert data['username'][0] == 'String value is too short.'
    elif not data.get('username', False) and data.get('password', False):
        assert data['password'][0] == 'String value is too short.'
    else:
        assert data['username'][0] == 'String value is too short.'
        assert data['password'][0] == 'String value is too short.'
