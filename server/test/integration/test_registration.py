import pytest

bad_username_password = [
    ('te', '12'),
    ('test_username', '12'),
    ('te', '12345')
]


async def test_correct(client, user_object):
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


async def test_user_already_exists(client, user_object, drop_user):
    response = await client.post(
        '/api/registration',
        json={
            'username': user_object.username,
            'password': user_object.password
        }
    )
    assert response.status == 409
    data = await response.json()
    assert data['message'] == 'user with that name already exists'


@pytest.mark.parametrize('username, password', bad_username_password)
async def test_validation_error(username, password, client, event_loop):
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
