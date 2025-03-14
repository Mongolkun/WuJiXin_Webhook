from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from db import connect_db
from utils import markdown_to_html
import os

HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "posts")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    await update.message.reply_text("Привет! Это WuJiXing Telegram Bot 🚀")

# /help
async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT command, response FROM {HELP_TABLE}")
    if rows:
        help_text = "\n".join([f"{row['command']}: {row['response']}" for row in rows])
        await update.message.reply_text(help_text)
    else:
        await update.message.reply_text("❌ В базе пока нет команд.")

# /info
async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT topic, description FROM {INFO_TABLE}")
    if rows:
        info_text = "\n".join([f"{row['topic']}: {row['description']}" for row in rows])
        await update.message.reply_text(info_text)
    else:
        await update.message.reply_text("❌ В базе пока нет информации.")

# /random
async def send_random_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(f"SELECT content FROM {POST_TABLE} WHERE lang = 'ru' ORDER BY RANDOM() LIMIT 1")

    if row:
        text = markdown_to_html(row['content'])
        await update.message.reply_text(text, parse_mode="HTML")
    else:
        await update.message.reply_text("❌ В базе пока нет постов.")

# Регистрация команд
def register_handlers(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", send_help))
    application.add_handler(CommandHandler("info", send_info))
    application.add_handler(CommandHandler("random", send_random_post))
