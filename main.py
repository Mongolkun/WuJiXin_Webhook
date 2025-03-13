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
HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

import re

def markdown_to_html(text):
    """Конвертирует MarkdownV2 в HTML перед отправкой в Telegram"""
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Жирный → <b>Жирный</b>
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)  # *Курсив* → <i>Курсив</i>
    text = re.sub(r"(.*?)(.*?)", r'<a href="\2">\1</a>', text)  # [Текст](ссылка) → <a href="ссылка">Текст</a>

    text = text.replace("\n", "<br>")  # Telegram использует <br> вместо \n

    return text

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

# Команда /start
async def send_random_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбираем случайный пост, форматируем и отправляем в Telegram"""
    pool = await connect_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(f"SELECT content FROM posts WHERE lang = 'ru' ORDER BY RANDOM() LIMIT 1")

    if row:
        text = markdown_to_html(row['content'])  # ✅ Конвертируем MarkdownV2 → HTML
        await update.message.reply_text(text, parse_mode="HTML")  # ✅ Telegram поймёт формат
    else:
        await update.message.reply_text("❌ В базе пока нет постов.")

# Команда /help - получение справки

async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT command, response FROM {HELP_TABLE}")
    if rows:
        help_text = "\n".join([f"{row['command']}: {row['response']}" for row in rows])
        await update.message.reply_text(help_text)
    else:
        await update.message.reply_text("❌ В базе пока нет команд.")
        
async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT topic, description FROM {INFO_TABLE}")
    info_text = "\n".join([f"{row['topic']}: {row['description']}" for row in rows])
    await update.message.reply_text(info_text)

async def send_random_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбираем случайный пост, форматируем и отправляем в Telegram"""
    pool = await connect_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(f"SELECT content FROM posts WHERE lang = 'ru' ORDER BY RANDOM() LIMIT 1")

    if row:
        text = markdown_to_html(row['content'])  # ✅ Конвертируем MarkdownV2 → HTML
        await update.message.reply_text(text, parse_mode="HTML")  # ✅ Telegram поймёт формат
    else:
        await update.message.reply_text("❌ В базе пока нет постов.")

bot_builder.add_handler(CommandHandler("start", start))
bot_builder.add_handler(CommandHandler("help", send_help))
bot_builder.add_handler(CommandHandler("info", send_info))
bot_builder.add_handler(CommandHandler("random", send_random_post))
