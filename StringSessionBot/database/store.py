from datetime import datetime, timezone
from pymongo import MongoClient
from env import MONGODB_URI

_client = None
_db = None

def get_database():
    global _client, _db
    if not MONGODB_URI:
        return None
    if _db is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        _db = _client.get_default_database()
        _db.bot_users.create_index("user_id", unique=True)
    return _db

async def record_user(user_id, username):
    database = get_database()
    if database is None:
        return
    now = datetime.now(timezone.utc)
    database.bot_users.update_one(
        {"user_id": user_id},
        {
            "$set": {"username": username, "last_seen": now},
            "$setOnInsert": {"first_seen": now},
        },
        upsert=True,
    )
