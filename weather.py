import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

API_TOKEN = "8492691594:AAFSmXXPnv3lL_SEwyJJs9rumwQtisM7r_U"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("weather"))
async def get_weather(message: Message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 1:
            city = "Almaty"
        else:
            city = parts[1]

        # Получаем координаты
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_resp = requests.get(geo_url, timeout=5)

        if geo_resp.status_code != 200:
            await message.answer("Ошибка: не удалось получить координаты 😢")
            return

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

        if weather_resp.status_code != 200:
            await message.answer("Ошибка: не удалось получить погоду 😢")
            return

        weather_data = weather_resp.json()
        current = weather_data.get("current_weather")

        if not current:
            await message.answer("Не удалось получить данные о погоде 😢")
            return

        temp = current["temperature"]
        wind = current["windspeed"]

        reply_text = (
            f"🌤 Погода в {city_name}:\n"
            f"Температура: {temp}°C\n"
            f"Ветер: {wind} м/с"
        )

        await message.answer(reply_text)

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при получении данных.")
        print(e)


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
