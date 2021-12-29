import logging
import os

from motor import motor_asyncio


DB_CONNECTION = None
DATABASE = None
log = logging.getLogger(__name__)


def db_connection():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        mongo_url = os.environ['MONGO_URL']
        DB_CONNECTION = motor_asyncio.AsyncIOMotorClient(mongo_url)
    return DB_CONNECTION


def db() -> motor_asyncio.AsyncIOMotorDatabase:
    global DATABASE
    if DATABASE is None:
        mongo_database = os.environ['MONGO_DATABASE']
        DATABASE = db_connection()[mongo_database]
    return DATABASE


async def read_name() -> dict:
    obj = await db().rooms.find_one({'name': 'Вадик?'})
    return obj


async def create_room(data: dict):
    await db().rooms.insert_one(data)


async def get_rooms(page: int, limit: int) -> (list, int):
    cursor = db().rooms.aggregate([
        {"$limit": limit},
        {"$skip": (page - 1) * limit},
    ])
    return await cursor.to_list(None), await db().rooms.count_documents({})  # return rooms, total_count
