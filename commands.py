from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from db import connect_db, HELP_TABLE, INFO_TABLE, POST_TABLE
import os
import re

def markdown_to_html(text):
    """Конвертирует MarkdownV2 в HTML перед отправкой в Telegram"""
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Жирный → <b>Жирный</b>
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)  # *Курсив* → <i>Курсив</i>

    # ✅ Исправленный код для ссылок [Текст](https://example.com) → <a href="URL">Текст</a>
    text = re.sub(r"\[(.*?)\]\((https?:\/\/[^\)]+)\)", r'<a href="\2">\1</a>', text)

    text = text.replace("|", "\n")  # Telegram использует \n вместо |

    return text

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    start_text = "Привет! Это **WuJiXing Telegram Bot** 🚀"
    start_text = markdown_to_html(start_text)  # ✅ Конвертируем MarkdownV2 → HTML
    await update.message.reply_text(start_text, parse_mode="HTML")

# Команда /help - получение справки
async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT command, response FROM {HELP_TABLE}")
    if rows:
        help_text = "\n".join([f"{row['command']}: {row['response']}" for row in rows])
        help_text = markdown_to_html(help_text)  # ✅ Конвертируем MarkdownV2 → HTML
        await update.message.reply_text(help_text, parse_mode="HTML")
    else:
        await update.message.reply_text("❌ В базе пока нет команд.")

# Команда /info - получение информации
async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT topic, description FROM {INFO_TABLE}")
    if rows:
        info_text = "\n".join([f"{row['topic']}: {row['description']}" for row in rows])
        info_text = markdown_to_html(info_text)  # ✅ Конвертируем MarkdownV2 → HTML
        await update.message.reply_text(info_text, parse_mode="HTML")
    else:
        await update.message.reply_text("❌ В базе пока нет информации.")

# Команда /random - получение случаного поста
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
        
def register_handlers(bot_builder):
    bot_builder.add_handler(CommandHandler("start", start))
    bot_builder.add_handler(CommandHandler("help", send_help))
    bot_builder.add_handler(CommandHandler("info", send_info))
    bot_builder.add_handler(CommandHandler("random", send_random_post))
