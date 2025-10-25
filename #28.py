import logging
import time
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_TOKEN = "8492691594:AAHGomYK8lOc-AUGzJ-PtHGopAixKsPOlI0"

# 🔹 Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

# 🔹 Функция для логирования API-запросов
def log_api_request(url: str, start_time: float, success: bool, error: str = None):
    duration = time.time() - start_time
    if duration > 1:
        logger.warning(f"Долгий ответ API: {url} ({duration:.2f} сек)")
    if success:
        logger.info(f"Успешный запрос: {url} ({duration:.2f} сек)")
    else:
        logger.error(f"Ошибка API при запросе {url}: {error}")

# 🔹 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь вошёл: ID={user.id}, Имя={user.first_name}, Время={datetime.now()}")
    await update.message.reply_text(f"Привет, {user.first_name}! 👋\nВыбери сценарий: /weather или /quote")

# 🔹 Команда /weather (пример API-запроса)
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.id} выбрал сценарий: Погода")

    url = "https://api.open-meteo.com/v1/forecast?latitude=51.17&longitude=71.45&current_weather=true"
    start_time = time.time()

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp = data["current_weather"]["temperature"]
        await update.message.reply_text(f"🌤 Сейчас температура {temp}°C")
        log_api_request(url, start_time, success=True)
    except Exception as e:
        await update.message.reply_text("⚠ Не удалось получить данные о погоде.")
        log_api_request(url, start_time, success=False, error=str(e))

# 🔹 Команда /quote (пример API-запроса)
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.id} выбрал сценарий: Цитата")

    urls = [
        "https://api.quotable.io/random",
        "https://zenquotes.io/api/random"  # запасной вариант
    ]

    for url in urls:
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Разные API — разная структура
            if "content" in data:
                text = data["content"]
                author = data["author"]
            elif isinstance(data, list) and "q" in data[0]:
                text = data[0]["q"]
                author = data[0]["a"]
            else:
                raise ValueError("Неожиданная структура данных")

            await update.message.reply_text(f"💬 {text}\n— {author}")
            log_api_request(url, start_time, success=True)
            return

        except Exception as e:
            log_api_request(url, start_time, success=False, error=str(e))

    await update.message.reply_text("⚠ Не удалось получить цитату, попробуйте позже.")


# 🔹 Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен 🚀")
    try:
        app = ApplicationBuilder().token(API_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("weather", weather))
        app.add_handler(CommandHandler("quote", quote))

        app.run_polling()
    finally:
        logger.info("Бот остановлен 🛑")
