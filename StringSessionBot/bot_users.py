from .database.store import record_user

async def touch_user(user):
    await record_user(user.id, user.username)
