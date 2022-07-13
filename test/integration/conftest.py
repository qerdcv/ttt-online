import typing as t

import pytest
from aiohttp.test_utils import TestClient

from src.app import create_app
from src import db
from src.models.user import User
from src.models.game import Game


@pytest.fixture(autouse=True)
async def set_up():
    # Put code here
    yield


@pytest.fixture(autouse=True)
async def therdown(client: TestClient):
    yield
    await client.get('/api/logout')
    await db.cleanup(client.app['pool'])


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    client = await aiohttp_client(create_app())
    yield client
    await client.app['pool'].close()


@pytest.fixture
def user_object() -> User:
    return User(
        {
            'username': 'test_user',
            'password': '12345'
        }
    )


@pytest.fixture
def user_opponent_object(user_object: User) -> User:
    return User(
        {
            'username': user_object.username + '_opponent',
            'password': str(user_object.password)
        }
    )


@pytest.fixture
async def game_object(client: TestClient, test_user: User) -> Game:
    return await db.create_game(
        client.app['pool'],
        test_user
    )


@pytest.fixture
async def game_with_opponent(client: TestClient, game_object: Game, test_opponent: User) -> Game:
    game_object.set_opponent(test_opponent)
    await db.update_game(
        client.app['pool'],
        game_object
    )
    return game_object


@pytest.fixture
async def test_user(client: TestClient, user_object: User) -> User:
    await db.create_user(
        client.app['pool'],
        user_object
    )
    return user_object


@pytest.fixture
async def test_opponent(client: TestClient, user_opponent_object: User) -> User:
    await db.create_user(
        client.app['pool'],
        user_opponent_object
    )
    return user_opponent_object


@pytest.fixture
async def logged_user(client: TestClient, test_user: User) -> User:
    await client.post(
        '/api/login',
        json={
            'username': test_user.username,
            'password': test_user.password
        }
    )
    yield test_user
    await client.get('/api/logout')


@pytest.fixture
async def logged_user_opponent(client: TestClient, test_opponent: User) -> User:
    await client.post(
        '/api/login',
        json={
            'username': test_opponent.username,
            'password': test_opponent.password
        }
    )
    yield test_opponent
    await client.get('/api/logout')


@pytest.fixture
async def game_factory(client: TestClient, test_user: User) \
        -> t.Callable[[int], t.Awaitable[None]]:
    async def create_games(count: int):
        for _ in range(count):
            await db.create_game(
                client.app['pool'],
                await db.get_user(client.app['pool'], test_user)
            )
    return create_games


@pytest.fixture
async def login_user(client: TestClient) -> t.Callable[[User], t.Awaitable[User]]:
    async def logged_user(user: User):
        await client.post(
            '/api/login',
            json={
                'username': user.username,
                'password': user.password
            }
        )
        return user
    return logged_user


@pytest.fixture
async def update_game(client: TestClient) -> t.Callable[[Game], t.Awaitable[None]]:
    async def wrapped(game: Game):
        await db.update_game(client.app['pool'], game)
    return wrapped
