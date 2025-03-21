from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from db import connect_db, HELP_TABLE, INFO_TABLE, POST_TABLE
import os
import re
import gc
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    start_text = """Приветствую тебя, Путник! 

Ты вошёл в пространство <b>WuJiXing Quotes</b> — цифровое место, где цитаты и вопросы помогают открыть новые горизонты мышления.

🔹 Задай свой вопрос и получи случайную мысль с помощью команды <b>/random</b>.  
🔹 Используй <b>/help</b> или открой <b>Меню</b>, если нужна помощь с навигацией.  

Здесь каждый шаг ведёт к новому пониманию.
<b>Двигайся, и путь откроется сам</b>.
"""

    start_text = markdown_to_html(start_text)  # ✅ Конвертируем MarkdownV2 → HTML
    await update.message.reply_text(start_text, parse_mode="HTML")

# Команда /help - получение справки
async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводит список доступных команд"""
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT command, response FROM {HELP_TABLE}")
    
    await pool.close()

    if rows:
        help_text = "\n".join([f"{row['command']}: {row['response']}" for row in rows])
        final_text = f"Путник, тебе доступны следующие команды:\n\n{help_text}"
        await update.message.reply_text(final_text)
    else:
        await update.message.reply_text("❌ В базе пока нет команд.")

# Команда /info - получение информации
async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool = await connect_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"SELECT topic, description FROM {INFO_TABLE}")
    await pool.close()  # ✅ Закрываем соединение после работы с БД
    gc.collect()  # ✅ Принудительная очистка памяти
    
    if rows:
        info_text = "\n".join([f"{row['topic']}: {row['description']}" for row in rows])
        info_text = markdown_to_html(info_text)  # ✅ Конвертируем MarkdownV2 → HTML
        await update.message.reply_text(info_text, parse_mode="HTML")
    else:
        await update.message.reply_text("❌ В базе пока нет информации.")


# Команда /random - получение случаного поста
async def send_random_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("📡 Вызвана команда /random")
    pool = await connect_db()
    if not pool:
        logging.error("❌ Ошибка: нет соединения с базой!")
        await update.message.reply_text("❌ Ошибка: База данных недоступна!")
        return
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(f"SELECT id, thread, language, date FROM posts WHERE language = 'ru' ORDER BY RANDOM() LIMIT 1") 

        if not row:
            logging.error("❌ Ошибка: SQL-запрос не вернул строку!")
            await update.message.reply_text("❌ В базе пока нет постов.")
            return
        
        post_id = row["id"]
        thread_id = row["thread"]
        language = row["language"]
        post_date = row["date"]

        if thread_id == 0:  # Одиночный пост
            post = await conn.fetchrow(f"SELECT content, category FROM posts WHERE id = {post_id} AND language = '{language}'")
            content = markdown_to_html(post["content"])
            category = post["category"]
            await update.message.reply_text(f"{content}\n\n#WuJiXing #{category}", parse_mode="HTML")
        
        else:  # Пост в треде с задержкой 1 секунда между сообщениями
            posts = await conn.fetch(f"""
                SELECT content, position, category FROM posts 
                WHERE thread = {thread_id} AND language = '{language}' AND date = '{post_date}'
                ORDER BY position
            """)
            category = posts[-1]["category"]  # Берём категорию из последнего поста

            for i, post in enumerate(posts):
                content = markdown_to_html(post["content"])
                if i == len(posts) - 1:  # Последний пост в треде
                    content += f"\n\n#WuJiXing #{category}"
                await update.message.reply_text(content, parse_mode="HTML")
                
                if i < len(posts) - 1:  # Добавляем задержку перед следующими постами
                    await asyncio.sleep(1)
    await pool.close()

#Обработчик неизвестных команд
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Автоответ, если команда не распознана"""
    await update.message.reply_text(
        "Путник, я не знаю этой команды.\n"
        "Но ты можешь использовать основные команды:\n"
        "🔹 /start – Начать общение\n"
        "🔹 /help – Посмотреть список команд\n"
        "🔹 /random – Получить случайную мысль **WuJiXing**\n"
        "🔹 /info – Узнать больше о проекте **WuJiXing**",
        parse_mode="HTML"
    )

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Автоответ, если пользователь пишет обычное сообщение"""
    await update.message.reply_text(
        "Путник, сейчас я не умею вести беседу.\n"
        "Но, возможно, однажды наши диалоги станут глубже.\n\n"
        "Пока используй команду:\n"
        "🔹 /help – Список доступных команд",
        parse_mode="HTML"
    )
    
def register_handlers(bot_builder):
    bot_builder.add_handler(CommandHandler("start", start))
    bot_builder.add_handler(CommandHandler("help", send_help))
    bot_builder.add_handler(CommandHandler("info", send_info))
    bot_builder.add_handler(CommandHandler("random", send_random_post))
    bot_builder.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    bot_builder.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
