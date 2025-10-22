import asyncio
import httpx
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "8492691594:AAEZiDIaK7_MdZNbK-qb3HHUC1bZiwrL-48"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- КЭШ ДЛЯ ЗАПРОСОВ ---
cache = {}

# --- ПОЛУЧЕНИЕ ПОГОДЫ ---
async def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        current = data["current_condition"][0]
        temp = int(current["temp_C"])
        desc = current["weatherDesc"][0]["value"]
        emoji = "🔥" if temp > 25 else "❄️" if temp < 0 else "🌤️"
        return {"city": city, "temp": temp, "desc": desc, "emoji": emoji}

# --- ПОЛУЧЕНИЕ КУРСОВ ВАЛЮТ ---
async def get_currency():
    url = "https://open.er-api.com/v6/latest/USD"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        if "rates" not in data:
            raise ValueError("Некорректный ответ от API валют")
        return data["rates"]

# --- СОЗДАНИЕ КАРТОЧКИ ---
def format_card(weather, currency):
    now = time.strftime("%H:%M:%S")
    usd_kzt = round(currency["KZT"], 2)
    eur_kzt = round(currency["EUR"], 2)
    rub_kzt = round(currency["RUB"], 2)

    return (
        f"{weather['emoji']} <b>Город:</b> {weather['city']}\n"
        f"🌡 <b>Температура:</b> {weather['temp']}°C\n"
        f"☁️ <b>Погодa:</b> {weather['desc']}\n\n"
        f"💵 <b>Курсы валют:</b>\n"
        f"USD → {usd_kzt} ₸\n"
        f"EUR → {eur_kzt} ₸\n"
        f"RUB → {rub_kzt} ₸\n\n"
        f"⏱ <i>Обновлено: {now}</i>\n\n"
        f"<a href='https://wttr.in'>Погода</a> | <a href='https://exchangerate.host'>Валюты</a>"
    )

# --- КНОПКИ ---
def get_buttons():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Обновить", callback_data="refresh")
    kb.button(text="🌆 Выбрать город", callback_data="choose_city")
    kb.adjust(2)
    return kb.as_markup()

# --- ОСНОВНАЯ ФУНКЦИЯ ЗАПРОСА ---
async def fetch_data(city: str):
    now = time.time()
    if city in cache and now - cache[city]["time"] < 60:
        return cache[city]["data"]

    weather, currency = await asyncio.gather(get_weather(city), get_currency())
    cache[city] = {"data": (weather, currency), "time": now}
    return weather, currency

# --- КОМАНДА /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я показываю погоду и курс валют.\n\nИспользуй команду /info или кнопки ниже.",
        reply_markup=get_buttons(),
    )

# --- КОМАНДА /info ---
@dp.message(Command("info"))
async def info(message: types.Message):
    city = "Aktobe"
    try:
        weather, currency = await fetch_data(city)
        text = format_card(weather, currency)
        await message.answer(text, reply_markup=get_buttons())
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# --- ОБРАБОТКА КНОПКИ 🔄 Обновить ---
@dp.callback_query(F.data == "refresh")
async def refresh_callback(callback: types.CallbackQuery):
    city = "Aktobe"
    try:
        weather, currency = await fetch_data(city)
        text = format_card(weather, currency)
        await callback.message.edit_text(text, reply_markup=get_buttons())
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при обновлении: {e}")

# --- ОБРАБОТКА КНОПКИ 🌆 Выбрать город ---
@dp.callback_query(F.data == "choose_city")
async def choose_city(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    for c in ["Aktobe", "Almaty", "Astana", "Moscow", "London"]:
        kb.button(text=c, callback_data=f"city_{c}")
    kb.adjust(2)
    await callback.message.edit_text("🌆 Выбери город:", reply_markup=kb.as_markup())

# --- ВЫБОР ГОРОДА ---
@dp.callback_query(F.data.startswith("city_"))
async def city_selected(callback: types.CallbackQuery):
    city = callback.data.split("_")[1]
    try:
        weather, currency = await fetch_data(city)
        text = format_card(weather, currency)
        await callback.message.edit_text(text, reply_markup=get_buttons())
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")

# --- ЗАПУСК ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
