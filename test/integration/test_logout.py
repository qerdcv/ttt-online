from aiohttp.test_utils import TestClient


async def test_correct(client: TestClient):
    response = await client.get('/api/logout')
    assert response.status == 200
    data = await response.json()
    assert data['message'] == 'OK'
    assert '0' == response.cookies["token"]["max-age"]
