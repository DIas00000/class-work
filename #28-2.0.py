import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "8492691594:AAHGomYK8lOc-AUGzJ-PtHGopAixKsPOlI0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================ ГЛАВНОЕ МЕНЮ ================
def main_menu():
    keyboard = [
        [InlineKeyboardButton(text="📅 Курс валют", callback_data="currency")],
        [InlineKeyboardButton(text="🎬 Случайный фильм", callback_data="movie")],
        [InlineKeyboardButton(text="☁️ Погода", callback_data="weather_astana")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Привет! Я мультисценарный бот.\nВыбери действие:", reply_markup=main_menu())


# ================ КУРС ВАЛЮТ ================
def get_currency():
    try:
        data = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        kzt = data["rates"]["KZT"]
        eur = data["rates"]["EUR"]
        rub = data["rates"]["RUB"]
        return f"💵 Курс валют (относительно USD):\n\n🇰🇿 KZT: {kzt:.2f}\n🇪🇺 EUR: {eur:.2f}\n🇷🇺 RUB: {rub:.2f}"
    except Exception as e:
        return f"Ошибка при получении данных: {e}"


def small_menu(prefix):
    keyboard = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"{prefix}_refresh")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.callback_query(F.data == "currency")
async def show_currency(callback: CallbackQuery):
    await callback.message.edit_text(get_currency(), reply_markup=small_menu("currency"))


@dp.callback_query(F.data == "currency_refresh")
async def refresh_currency(callback: CallbackQuery):
    await callback.message.edit_text(get_currency(), reply_markup=small_menu("currency"))


# ================ СЛУЧАЙНЫЙ ФИЛЬМ (БЕЗ API-КЛЮЧА) ================
def get_random_movie():
    try:
        # Берём случайный жанр (добавляем разнообразие)
        genres = ["action-adventure", "comedy", "drama", "animation", "horror"]
        genre = random.choice(genres)
        url = f"https://api.sampleapis.com/movies/{genre}"
        data = requests.get(url, timeout=5).json()

        if not data:
            return "❌ Не удалось получить список фильмов."

        movie = random.choice(data)
        title = movie.get("title", "Без названия")
        year = movie.get("year", "N/A")
        desc = movie.get("description", "Описание отсутствует.")
        return f"🎬 {title} ({year})\n\n{desc}"
    except Exception as e:
        return f"Ошибка при получении фильма: {e}"


@dp.callback_query(F.data == "movie")
async def show_movie(callback: CallbackQuery):
    await callback.message.edit_text(get_random_movie(), reply_markup=small_menu("movie"))


@dp.callback_query(F.data == "movie_refresh")
async def refresh_movie(callback: CallbackQuery):
    await callback.message.edit_text(get_random_movie(), reply_markup=small_menu("movie"))


# ================ ПОГОДА (Open-Meteo, без ключа) ================
CITIES = {
    "astana": {"name": "Астана", "lat": 51.1694, "lon": 71.4491},
    "almaty": {"name": "Алматы", "lat": 43.2389, "lon": 76.8897},
    "shymkent": {"name": "Шымкент", "lat": 42.3417, "lon": 69.5901}
}

def get_weather(city_key: str):
    try:
        city = CITIES[city_key]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current_weather=true"
        data = requests.get(url, timeout=5).json()
        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]
        return f"🌆 {city['name']}\n🌡 Температура: {temp}°C\n💨 Ветер: {wind} км/ч"
    except Exception as e:
        return f"Ошибка при получении погоды: {e}"


def city_menu(selected_city):
    keyboard = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"weather_{selected_city}")],
        [InlineKeyboardButton(text="🏙 Изменить город", callback_data="change_city")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.callback_query(F.data.startswith("weather_"))
async def show_weather(callback: CallbackQuery):
    city_key = callback.data.split("_")[1]
    await callback.message.edit_text(get_weather(city_key), reply_markup=city_menu(city_key))


@dp.callback_query(F.data == "change_city")
async def choose_city(callback: CallbackQuery):
    keyboard = [[InlineKeyboardButton(text=info["name"], callback_data=f"weather_{key}")]
                for key, info in CITIES.items()]
    keyboard.append([InlineKeyboardButton(text="🏠 В меню", callback_data="to_menu")])
    await callback.message.edit_text("Выберите город:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


# ================ В МЕНЮ ================
@dp.callback_query(F.data == "to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("📋 Главное меню", reply_markup=main_menu())


# ================ ЗАПУСК ================
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
