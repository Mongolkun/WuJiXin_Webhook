import asyncpg
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Подключение к PostgreSQL
async def connect_db():
    return await asyncpg.create_pool(os.getenv("DATABASE_URL"))

# Команда /sttart
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    await update.message.reply_text("Привет! Это WuJiXing Telegram Bot 🚀")

# Команда /help - получение справки
async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT command, response FROM help")
    help_text = "\\n".join([f"{row['command']}: {row['response']}" for row in rows])
    await update.message.reply_text(help_text)

# Команда /info - получение информации о проекте
async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT topic, description FROM info")
    info_text = "\\n".join([f"{row['topic']}: {row['description']}" for row in rows])
    await update.message.reply_text(info_text)

# Команда /random - получение случайного поста
async def send_random_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT content FROM post ORDER BY RANDOM() LIMIT 1")
    if row:
        await update.message.reply_text(row['content'])
    else:
        await update.message.reply_text("В базе пока нет постов.")

# Регистрация команд в Telegram боте
def register_handlers(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", send_help))
    application.add_handler(CommandHandler("info", send_info))
    application.add_handler(CommandHandler("random", send_random_post))
