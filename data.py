from StringSessionBot.database.store import get_pool

async def init_database():
    pool = await get_pool()
    if not pool:
        return
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS bot_users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                first_seen TIMESTAMPTZ DEFAULT NOW(),
                last_seen TIMESTAMPTZ DEFAULT NOW()
            )
        ''')
