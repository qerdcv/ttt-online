import pytest
from aiohttp.test_utils import TestClient

from src.models.user import User
from src.encrypt import decode_jwt
from src.db import get_user


async def test_correct(client: TestClient, test_user: User):
    response = await client.post(
        '/api/login',
        json={
            'username': test_user.username,
            'password': test_user.password
        }
    )
    print(response.headers)
    assert response.status == 200
    data = await response.json()
    assert data['message'] == 'OK'
    assert 'token' in response.cookies
    user_info = decode_jwt(response.cookies.get('token').value)
    test_user_stored = await get_user(client.app['pool'], test_user)
    assert test_user_stored.id == user_info['id']
    assert test_user_stored.username == user_info['username']


async def test_wrong_password(client: TestClient, test_user: User):
    response = await client.post(
        '/api/login',
        json={
            'username': test_user.username,
            'password': test_user.password + 'a'
        }
    )
    assert response.status == 400
    data = await response.json()
    assert data['message'] == 'wrong password'


async def test_user_dont_exists(client: TestClient, test_user: User):
    response = await client.post(
        '/api/login',
        json={
            'username': test_user.username + 'a',
            'password': test_user.password
        }
    )
    assert response.status == 404
    data = await response.json()
    assert data['message'] == 'user don\'t exists'


# TODO: refactor for max size password or username
@pytest.mark.parametrize('username, password', [
    ('te', '12'),
    ('test_username', '12'),
    ('te', '12345')
])
async def test_validation_error(username: str, password: str, client: TestClient):
    response = await client.post(
        '/api/login',
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
