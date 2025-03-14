import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

async def connect_db():
    """Подключение к PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
