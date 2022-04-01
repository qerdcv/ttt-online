async def test_ping(client):
    response = await client.get('/ping')
    assert response.status == 200
    data = await response.json()
    assert data['message'] == 'pong'
