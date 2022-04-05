from aiohttp.test_utils import TestClient


async def test_success(client: TestClient):
    response = await client.get('/ping')
    assert response.status == 200
    data = await response.json()
    assert data['message'] == 'pong'
