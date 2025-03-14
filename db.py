import asyncpg
import os

print("📡 Загружается db.py...")  # Проверяем, вызывается ли вообще этот файл

async def connect_db():
    """ Подключение к PostgreSQL """
    print("📡 Подключаемся к базе данных...")  # Должно появиться в логах Railway
    print(f"📡 DATABASE_URL: {os.getenv('DATABASE_URL')}")
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))
