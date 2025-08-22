import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Берем ключи из переменных окружения (Render → Settings → Environment)
BOT_TOKEN = os.getenv("8464241048:AAE6vWcWEO_NtOAKKmS5NilBdpgE_WRRi24")
OPENROUTER_API_KEY = os.getenv("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")

# Проверка: если токенов нет — бот не запустится
if not BOT_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Не найдены BOT_TOKEN или OPENROUTER_API_KEY в переменных окружения!")

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я умный бот 🤖. Напиши мне что-нибудь!")

# Основная функция обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": user_message}]
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"Ошибка OpenRouter: {response.text}"

    except Exception as e:
        reply = f"Что-то пошло не так: {e}"

    await update.message.reply_text(reply)

# Главная функция запуска бота
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
