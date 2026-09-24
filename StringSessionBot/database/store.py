import asyncpg
from env import DATABASE_URL

_pool = None

async def get_pool():
    global _pool
    if not DATABASE_URL:
        return None
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=3)
        async with _pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS bot_users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_seen TIMESTAMPTZ DEFAULT NOW(),
                    last_seen TIMESTAMPTZ DEFAULT NOW()
                )
            ''')
    return _pool

async def record_user(user_id, username):
    pool = await get_pool()
    if not pool:
        return
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO bot_users(user_id, username)
            VALUES($1,$2)
            ON CONFLICT(user_id) DO UPDATE SET
              username=EXCLUDED.username, last_seen=NOW()
        ''', user_id, username)
