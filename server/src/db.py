import os

from motor import motor_asyncio


DB_CONNECTION = None
DATABASE = None


def db_connection():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        DB_CONNECTION = motor_asyncio.AsyncIOMotorClient(os.environ['MONGO_URL'])
    return DB_CONNECTION


def db() -> motor_asyncio.AsyncIOMotorDatabase:
    global DATABASE
    if DATABASE is None:
        DATABASE = db_connection()[os.environ['MONGO_DATABASE']]
    return DATABASE


async def create_room(data: dict):
    await db().rooms.insert_one(data)


async def get_rooms(page: int, limit: int) -> (list, int):
    cursor = db().rooms.aggregate([
        {"$limit": limit},
        {"$skip": (page - 1) * limit},
    ])
    return await cursor.to_list(None), await db().rooms.count_documents({})


async def room_is_occupied(data: dict) -> bool:
    obj = await db().rooms.find_one({"room_name": data["room_name"]})
    if obj is None:
        return False
    return True
