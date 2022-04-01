async def test_correct(client, test_user):
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
    is_cookie_exist = 'token' in response.headers.get('Set-Cookie')
    assert is_cookie_exist is True


async def test_wrong_password(client, test_user):
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
