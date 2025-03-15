# WuJiXing Telegram Bot v1.4 (Stable) 🚀

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed-Railway-blue?style=for-the-badge&logo=railway)

---

## 📌 Описание  
WuJiXing Bot — это Telegram-бот, работающий через Webhook.
- Выдаёт случайные цитаты WuJiXing из базы данных.
- Форматирует текст в HTML (жирный, курсив, ссылки).
- Обрабатывает треды и плавно выводит их с задержкой 1 секунда.
- Отвечает на неизвестные команды и обычные сообщения.
- Использует PostgreSQL для хранения данных.  

🔧 **Оптимизирован под Railway, минимум RAM: 78-82MB.**


💡 **Важно!**
- **Переменные окружения нужно присвоить ручной прописью в `.env` или Railway Variables!**
- **Таблицы PostgreSQL в репозиторий не входят!**

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
- **Убраны лишние соединения с базой (меньше нагрузки).**
- **Код /random переработан, теперь он быстрее обрабатывает SQL-запросы.** 

---

## 👤 Авторы  
- **Mongol.kun** — автор и разработчик WuJiXing.  
- **Gizmo (ChatGPT)** — технический ассистент, кодер и оптимизатор.
- **DangoDev** — автор оригинального шилона бота на Webhook (основан на DangoDev/TelegramBot.Webhook).
