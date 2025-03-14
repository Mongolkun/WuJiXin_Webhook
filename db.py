import asyncpg
import os
import logging
from dotenv import load_dotenv

load_dotenv()
HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

async def connect_db():
    """Подключение к PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logging.error("❌ Ошибка: DATABASE_URL не найден!")
        return None  

    logging.info("📡 Пытаемся подключиться к базе данных...")
    try:
        pool = await asyncpg.create_pool(database_url, min_size=1, max_size=5)
        logging.info("✅ Подключение к базе успешно!")
        return pool
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к базе: {e}")
        return None
