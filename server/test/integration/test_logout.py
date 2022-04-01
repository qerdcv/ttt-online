async def test_logout(client):
    response = await client.get('/api/logout')
    assert response.status == 200
    data = await response.json()
    assert data['message'] == 'OK'
