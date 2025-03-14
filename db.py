import asyncpg
import os

async def connect_db():
    """ Подключение к PostgreSQL """
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))
