import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def connect_db():
    """Подключение к PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Ошибка: DATABASE_URL не найден!")
        return None  # Возвращаем None, если переменная пустая

    print(f"📡 DATABASE_URL: {database_url}")

    try:
        pool = await asyncpg.create_pool(database_url)
        print("✅ База данных подключена успешно!")
        return pool
    except Exception as e:
        print(f"❌ Ошибка подключения к базе: {e}")
        return None  # Возвращаем None, если база не подключается
