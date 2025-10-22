import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
import asyncio

API_TOKEN = "8492691594:AAFSmXXPnv3lL_SEwyJJs9rumwQtisM7r_U"

# ✅ Новый способ задать parse_mode по умолчанию
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

CURRENCY_API_URL = "https://api.exchangerate.host/latest?base=USD&symbols=KZT,EUR,RUB"

def format_message(data: dict) -> str:
    rates = data.get("rates", {})
    usd = round(rates.get("KZT", 0), 2)
    eur = round(usd / 1.08, 2)
    rub = round(usd / 95, 2)

    message = (
        "<b>💵 Курсы валют (за 1 USD):</b>\n"
        f"USD → {usd} ₸\n"
        f"EUR → {eur} ₸\n"
        f"RUB → {rub} ₸\n\n"
        f"Источник: <a href='https://exchangerate.host'>exchangerate.host</a>"
    )
    return message


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! 👋 Напиши /rates, чтобы узнать актуальные курсы валют 💰")


@dp.message(Command("rates"))
async def cmd_rates(message: Message):
    response = requests.get(CURRENCY_API_URL)
    if response.status_code == 200:
        data = response.json()
        await message.answer(format_message(data))
    else:
        await message.answer("❌ Ошибка при получении данных. Попробуй позже.")


@dp.message(Command("format"))
async def cmd_format(message: Message):
    html_example = (
        "<b>Жирный</b>\n"
        "<i>Курсив</i>\n"
        "<u>Подчеркнутый</u>\n"
        "<a href='https://google.com'>Ссылка</a>\n"
        "<code>Код</code>"
    )
    await message.answer("🧱 Пример HTML форматирования:\n" + html_example)


async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
