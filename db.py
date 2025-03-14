import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

async def connect_db():
    """Подключение к PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return None  # Возвращаем None, если переменная пустая

    try:
        pool = await asyncpg.create_pool(database_url)
        return pool
    except Exception as e:
        return None  # Возвращаем None, если база не подключается
