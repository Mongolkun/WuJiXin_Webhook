import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application
from db import connect_db
from commands import register_handlers
import gc
from contextlib import asynccontextmanager

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Управление жизненным циклом Webhook'а Telegram """
    print("⚡ Сбрасываем старый Webhook...")
    await bot_builder.bot.deleteWebhook()  # Удаляем старый Webhook
    print("⚡ Устанавливаем новый Webhook...")
    await bot_builder.bot.setWebhook(url=WEBHOOK_DOMAIN)  # Устанавливаем новый Webhook

    yield  # ✅ Здесь должно быть yield, а не return

    print("⚡ Завершаем работу бота...")
    await bot_builder.stop()

app = FastAPI(lifespan=lifespan)

@app.post("/")
async def process_update(request: Request):
    """ Handles incoming Telegram updates and processes them with the bot. """
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_builder.bot)
    await bot_builder.process_update(update)
    gc.collect()  # ✅ Принудительная очистка памяти
    return Response(status_code=HTTPStatus.OK)
    
register_handlers(bot_builder)  # Теперь передаём bot_builder
