import asyncpg
import os



async def connect_db():
    """ Подключение к PostgreSQL """
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    await update.message.reply_text("Привет! Это WuJiXing Telegram Bot 🚀")
