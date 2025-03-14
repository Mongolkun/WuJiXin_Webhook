# WuJiXing Telegram Bot 🚀

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed-Railway-blue?style=for-the-badge&logo=railway)

---

## 📌 Описание  
WuJiXing Bot — это Telegram-бот, который обрабатывает MarkdownV2 и HTML, генерирует случайные цитаты и поддерживает форматирование текста.  

🔧 **Оптимизирован под Railway, минимум RAM: 78-82MB.**  

💡 **Важно!** Переменные окружения нужно присвоить ручной прописью в `.env` или Railway Variables!  

---

## ✨ Функционал  
- **FastAPI 🚀** — вебхуки Telegram работают на FastAPI.  
- **MarkdownV2 → HTML 🎨** — преобразует текст для Telegram.  
- **Случайные цитаты 🎲** — `/random` выбирает пост из базы.  
- **Поддержка ссылок 🔗** — `[URL](https://example.com)` превращается в `<a href="URL">URL</a>`.  

---

## 💁‍♂️ Как установить?  
```bash
git clone https://github.com/ТВОЙ_РЕПОЗИТОРИЙ
cd WuJiXingBot
pip install -r requirements.txt
hypercorn main:app --reload
```

---

## 🛠 Переменные окружения  
```plaintext
DATABASE_URL=postgresql://username:password@host:port/database
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
RAILWAY_PUBLIC_DOMAIN=https://your-app-name.up.railway.app
HELP_TABLE=help
INFO_TABLE=info
POST_TABLE=posts
```

---

## 🤖 Команды  
| Команда  | Описание  |
|-------------|-------------|
| `/start`    | Запуск бота  |
| `/help`     | Список команд  |
| `/random`   | Получить случайную цитату  |
| `/about`    | О боте и проекте  |

---

## 🔧 Оптимизация  
- **RAM: 78-82MB**  
- **Закрытие соединений с базой после каждого запроса**  
- **Webhook обновляется при запуске**  

---

## 👤 Авторы  
- **Mongol.kun** — автор и разработчик WuJiXing.  
- **Gizmo** — соразработчик и технический ассистент
