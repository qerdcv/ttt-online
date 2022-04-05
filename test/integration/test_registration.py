import typing as t

import pytest

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
