import pytest
from aiohttp.test_utils import TestClient

from src.app import create_app
from src import db
from src.models.user import User


@pytest.fixture(autouse=True)
async def set_up():
    # Put code here
    yield


@pytest.fixture(autouse=True)
async def therdown(client):
    yield
    await db.cleanup(client.app['pool'])


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    return await aiohttp_client(create_app())


@pytest.fixture
def user_object() -> User:
    return User(
        {
            'username': 'test_user',
            'password': '12345'
        }
    )


@pytest.fixture
async def test_user(client, user_object):
    await db.create_user(
        client.app['pool'],
        user_object
    )

    return user_object
