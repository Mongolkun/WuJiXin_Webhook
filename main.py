import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
# Импорт обработчиков команд


# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_DOMAIN: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# Build the Telegram Bot application
bot_builder = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)


# Подключение к PostgreSQL
async def connect_db():
    return await asyncpg.create_pool(os.getenv("DATABASE_URL"))

@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Sets the webhook for the Telegram Bot and manages its lifecycle (start/stop). """
    await bot_builder.bot.setWebhook(url=WEBHOOK_DOMAIN)
    async with bot_builder:
        await bot_builder.start()
        yield
        await bot_builder.stop()


app = FastAPI(lifespan=lifespan)

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

    bot_builder.add_handler(CommandHandler("start", start))
    bot_builder.add_handler(CommandHandler("help", send_help))
    bot_builder.add_handler(CommandHandler("info", send_info))
    bot_builder.add_handler(CommandHandler("random", send_random_post))
