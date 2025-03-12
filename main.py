import os
import asyncpg
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

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
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))

@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Sets the webhook for the Telegram Bot and manages its lifecycle (start/stop). """
    await bot_builder.bot.setWebhook(url=WEBHOOK_DOMAIN)
    async with bot_builder:
        await bot_builder.start()
        yield
        await bot_builder.stop()


app = FastAPI(lifespan=lifespan)

@app.post("/")
async def process_update(request: Request):
    """ Handles incoming Telegram updates and processes them with the bot. """
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_builder.bot)
    await bot_builder.process_update(update)
    return Response(status_code=HTTPStatus.OK)

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

async def get_db_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT current_database();")  # Получаем название базы
    await update.message.reply_text(f"База данных: {row['current_database']}")

async def check_env(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка, видит ли бот переменные окружения"""
    db_url = os.getenv("DATABASE_URL", "❌ DATABASE_URL не найден")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "❌ TEGRAM_BOT_TOKEN не найден")
    
    await update.message.reply_text(f"DATABASE_URL: {db_url}\nTOKEN: {bot_token}")


bot_builder.add_handler(CommandHandler("start", start))
bot_builder.add_handler(CommandHandler("help", send_help))
bot_builder.add_handler(CommandHandler("db_name", get_db_name))
bot_builder.add_handler(CommandHandler("check_env", check_env))
