import os
import random

from motor import motor_asyncio
from bson import ObjectId

from src.encrypt import encrypt
from src.settings import SECRET

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
    data['password'] = encrypt(key=SECRET, msg=data['password'])
    data.update({
        'game': {
            'player1': {
                'username': None,
                'mark': 'X'
            },
            'player2': {
                'username': None,
                'mark': '0'
            },
            'field': [
                [' ', ' ', ' '],
                [' ', ' ', ' '],
                [' ', ' ', ' ']
            ],
            'winner': '',
            'game_state': None,
            'start_time': None,
            'end_time': None
        }
    })
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


#  TODO: come up with another way to log in a user
async def login_room(data: dict):
    obj = await get_free_place(data)
    if obj is None:
        return False
    else:
        if len(obj) == 2:
            num_player = random.randint(1, 2)
        else:
            num_player = list(obj)[0][-1]
        await update_free_place(data, num_player)
        return True


async def update_free_place(data: dict, pos_player: int):
    await db().rooms.update_one(
        {"_id": ObjectId(data['room_id'])},
        {"$set":
            {
                f"game.player{pos_player}.username": data['user_name']
            }
        }
    )


async def get_free_place(data: dict) -> dict:
    obj = await db().rooms.find_one(
        {"_id": ObjectId(data['room_id'])},
        {
            "game.player1.username": 1,
            "game.player2.username": 1,
        }
    )
    result = {value: obj['game'][value] for value in obj['game'] if obj['game'][value]['username'] is None}
    return result if len(result) > 0 else None
