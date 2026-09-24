from StringSessionBot.database.store import get_database

def init_database():
    database = get_database()
    if database is None:
        return
    database.bot_users.create_index("user_id", unique=True)
