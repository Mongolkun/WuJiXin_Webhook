import asyncpg
import os

HELP_TABLE = os.getenv("HELP_TABLE", "help")
INFO_TABLE = os.getenv("INFO_TABLE", "info")
POST_TABLE = os.getenv("POST_TABLE", "post")

async def connect_db():
    """ Подключение к PostgreSQL """
    return await asyncpg.create_pool(os.getenv('DATABASE_URL'))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    await update.message.reply_text("Привет! Это WuJiXing Telegram Bot 🚀")

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
import re

def markdown_to_html(text):
    """Конвертирует MarkdownV2 в HTML перед отправкой в Telegram"""
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Жирный → <b>Жирный</b>
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)  # *Курсив* → <i>Курсив</i>

    # ✅ Исправленный код для ссылок [Текст](https://example.com) → <a href="URL">Текст</a>
    text = re.sub(r"\[(.*?)\]\((https?:\/\/[^\)]+)\)", r'<a href="\2">\1</a>', text)

    text = text.replace("|", "\n")  # Telegram использует \n вместо |

    return text

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
