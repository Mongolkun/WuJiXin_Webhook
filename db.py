import asyncpg
import os

HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

async def connect_db():
    """ Подключение к PostgreSQL """
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))
