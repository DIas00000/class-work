import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from requests.exceptions import Timeout, ConnectionError, HTTPError

# 🔹 Твой токен от BotFather
API_TOKEN = "8492691594:AAFSmXXPnv3lL_SEwyJJs9rumwQtisM7r_U"

# Настройка логирования ошибок
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# 🔹 Функция для получения цитаты с API
async def get_quote():
    url = "http://api.quotable.io/random"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return f"💬 {data['content']}\n\n👤 — {data['author']}"

    except Timeout:
        logging.error("⏰ Timeout — сервер не отвечает. Повтор запроса...")
        try:
            # 🔁 Повторяем запрос один раз
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return f"💬 {data['content']}\n\n👤 — {data['author']}"
        except Exception as e:
            logging.error(f"❌ Ошибка при повторном запросе: {e}")
            return "⏰ Сервер не отвечает даже после повторной попытки. Попробуй позже."

    except ConnectionError:
        logging.error("🚫 ConnectionError — нет подключения к интернету.")
        return "🚫 Нет подключения к интернету. Проверь сеть."

    except HTTPError:
        logging.error("⚠️ HTTPError — ошибка на стороне сервера.")
        return "⚠️ Ошибка на сервере. Попробуй позже."

    except Exception as e:
        logging.error(f"❌ Непредвиденная ошибка: {e}")
        return "❌ Что-то пошло не так. Попробуй позже."


# 🔹 Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет 👋\nНабери /quote, чтобы получить случайную цитату!"
    )


# 🔹 Команда /quote
@dp.message(Command("quote"))
async def quote_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Повторить запрос", callback_data="retry_quote")]
        ]
    )
    quote = await get_quote()
    await message.answer(quote, reply_markup=keyboard)


# 🔹 Обработка кнопки “🔄 Повторить запрос”
@dp.callback_query()
async def retry_quote(callback: types.CallbackQuery):
    if callback.data == "retry_quote":
        quote = await get_quote()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Повторить запрос", callback_data="retry_quote")]
            ]
        )
        await callback.message.answer(quote, reply_markup=keyboard)
        await callback.answer("🔁 Цитата обновлена!")


# 🔹 Запуск бота
async def main():
    print("🤖 Бот запущен и ждёт команды...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
