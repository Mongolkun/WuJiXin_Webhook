# WuJiXing Telegram Bot 🚀

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed-Railway-blue?style=for-the-badge&logo=railway)

---

## 📌 Описание
**WuJiXing Bot** — это Telegram-бот, который обрабатывает MarkdownV2 и HTML, генерирует случайные цитаты и поддерживает форматирование текста.  

Бот разрабатывается для проекта **WuJiXing** и поддерживает ссылки, жирный и курсивный текст.  

---

## ✨ Функционал
- **FastAPI** 🚀 — быстрый API для обработки вебхуков Telegram.  
- **MarkdownV2 → HTML** 🎨 — автоматическое преобразование текста перед отправкой.  
- **Переносы строк (`|` → `
`)** 📜 — Telegram корректно рендерит текст.  
- **Случайные цитаты** 🎲 — команда `/random` выбирает случайный пост из базы.  
- **Поддержка ссылок** 🔗 — `[Текст](https://example.com)` превращается в `<a href="URL">Текст</a>`.  
- **Работает с базами данных** 🗃️ (PostgreSQL, Railway) **⚠️** *База данных не входит в репозиторий!*  

---

## 💁‍♀️ Как установить?
1️⃣ Клонируем репозиторий:
```bash
git clone https://github.com/ТВОЙ_РЕПОЗИТОРИЙ
cd WuJiXingBot
```
2️⃣ Устанавливаем зависимости:
```bash
pip install -r requirements.txt
```
3️⃣ Запускаем локально:
```bash
hypercorn main:app --reload
```

---

## 🤖 Команды
| **Команда**  | **Описание**  |
|-------------|-------------|
| `/start`    | Запуск бота  |
| `/help`     | Список команд  |
| `/random`   | Получить случайную цитату  |
| `/about`    | О боте и проекте  |

---

## **👤 Авторы**
🔹 **Mongol.kun** — автор и разработчик WuJiXing.  
🔹 **Gizmo (ChatGPT)** — соразработчик, кодер и технический ассистент.  

---
