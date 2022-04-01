import asyncio

import pytest
from aiohttp.test_utils import TestClient

from src.app import create_app
from src import db
from src.models.user import User


@pytest.fixture(scope='session')
def client(event_loop: asyncio.AbstractEventLoop, aiohttp_client) -> TestClient:
    return event_loop.run_until_complete(aiohttp_client(create_app()))


@pytest.fixture
def user_object() -> User:
    return User(
        {
            'username': 'test_user',
            'password': '12345'
        }
    )


@pytest.fixture
async def drop_user(client, user_object, event_loop, request):
    def delete_user():
        async def delete():
            pool = client.app['pool']
            async with pool.acquire() as conn:
                await conn.execute(
                    "DELETE FROM users WHERE username=$1",
                    user_object.username
                )

        event_loop.run_until_complete(delete())

    request.addfinalizer(delete_user)
    return drop_user


@pytest.fixture
async def test_user(client, user_object, event_loop, request):
    await db.create_user(
        client.app['pool'],
        user_object
    )

    def delete_user():
        async def delete():
            pool = client.app['pool']
            async with pool.acquire() as conn:
                await conn.execute(
                    "DELETE FROM users WHERE username=$1",
                    user_object.username
                )
        event_loop.run_until_complete(delete())

    request.addfinalizer(delete_user)
    return test_user
