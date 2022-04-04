import typing as t

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


@pytest.mark.parametrize('username, password, expected_result', [
    ('te', '12', ('String value is too short.', 'String value is too short.')),
    ('test_username', '12', 'String value is too short.'),
    ('te', '12345', 'String value is too short.'),
    ('test_username' * 3, '1' * 31, ('String value is too long.', 'String value is too long.')),
    ('test_username' * 3, '12345', 'String value is too long.'),
    ('test_username', '1' * 31, 'String value is too long.'),
    ('te', '1' * 31, ('String value is too short.', 'String value is too long.')),
    ('test_username' * 3, '1', ('String value is too long.', 'String value is too short.'))
])
async def test_validation_error(username: str, password: str, expected_result: t.Union[str, tuple], client: TestClient):
    response = await client.post(
        '/api/registration',
        json={
            'username': username,
            'password': password
        }
    )
    assert response.status == 400
    data = await response.json()
    if isinstance(expected_result, tuple):
        assert data['username'][0] == expected_result[0]
        assert data['password'][0] == expected_result[1]
    else:
        if len(username) < 4 or len(username) > 30:
            assert data['username'][0] == expected_result
        else:
            assert data['password'][0] == expected_result
