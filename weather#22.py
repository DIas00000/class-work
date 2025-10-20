import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = "8492691594:AAFSmXXPnv3lL_SEwyJJs9rumwQtisM7r_U"  # ← вставь сюда токен от BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# 📜 Команда /quote — случайная цитата
@dp.message(Command("quote"))
async def send_quote(message: Message):
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5)
        data = response.json()
        quote = data["content"]
        author = data["author"]
        await message.answer(f"💬 {quote}\n\n— {author}")
    except Exception as e:
        print(e)
        await message.answer("⚠️ Не удалось получить цитату. Попробуй позже.")


# 🌤 Команда /weather <город>
@dp.message(Command("weather"))
async def get_weather(message: Message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 1:
            city = "Aktobe"  # по умолчанию
        else:
            city = parts[1]

        # Получаем координаты города
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_resp = requests.get(geo_url, timeout=5)
        geo_data = geo_resp.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            await message.answer("❌ Город не найден, попробуй другой.")
            return

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]

        # Получаем погоду
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_resp = requests.get(weather_url, timeout=5)
        weather_data = weather_resp.json()
        current = weather_data.get("current_weather")

        if not current:
            await message.answer("⚠️ Не удалось получить данные о погоде.")
            return

        temp = current["temperature"]
        wind = current["windspeed"]

        await message.answer(
            f"🌤 Погода в {city_name}:\nТемпература: {temp}°C\nВетер: {wind} м/с"
        )

    except Exception as e:
        print(e)
        await message.answer("⚠️ Произошла ошибка при получении погоды.")


# 🚀 Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
