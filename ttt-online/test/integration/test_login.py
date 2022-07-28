import typing as t

import pytest
from aiohttp.test_utils import TestClient

from src.models.user import User
from src.encrypt import decode_jwt


@pytest.mark.parametrize('remember, expected_max_age', [
    (True, ''),
    (False, '604800'),  # 604800 - 7 days in seconds
    (None, '604800')
])
async def test_success(client: TestClient, test_user: User,
                       remember: t.Optional[bool], expected_max_age: t.Optional[str]):
    response = await client.post(
        '/api/login',
        json={
            'username': test_user.username,
            'password': test_user.password,
            'remember': remember
        }
    )
    assert response.status == 200
    data = await response.json()
    assert data['id'] == test_user.id
    assert data['username'] == test_user.username
    assert 'token' in response.cookies
    user_info = decode_jwt(response.cookies.get('token').value)
    assert user_info['id'] == test_user.id
    assert user_info['username'] == test_user.username
    assert response.cookies['token']['max-age'] == expected_max_age


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
    ('te', '12', (['String value is too short.'], ['String value is too short.'])),
    ('test_username', '12', (None, ['String value is too short.'])),
    ('te', '12345', (['String value is too short.'], None)),
    ('test_username' * 3, '1' * 31, (['String value is too long.'], ['String value is too long.'])),
    ('test_username' * 3, '12345', (['String value is too long.'], None)),
    ('test_username', '1' * 31, (None, ['String value is too long.'])),
    ('te', '1' * 31, (['String value is too short.'], ['String value is too long.'])),
    ('test_username' * 3, '1', (['String value is too long.'], ['String value is too short.']))
])
async def test_validation_error(username: str, password: str, expected_result: tuple, client: TestClient):
    response = await client.post(
        '/api/login',
        json={
            'username': username,
            'password': password
        }
    )
    assert response.status == 400
    data = await response.json()
    assert (data.get('username'), data.get('password')) == expected_result
