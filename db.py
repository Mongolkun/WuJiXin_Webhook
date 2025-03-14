import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

print("📡 Загружается db.py...")  # Проверяем, вызывается ли вообще этот файл

async def connect_db():
    """ Подключение к PostgreSQL """
    print("📡 Подключаемся к базе данных...")  # Должно появиться в логах Railway
    print(f"📡 DATABASE_URL: {os.getenv('DATABASE_URL')}")
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))
