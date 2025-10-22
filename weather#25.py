import asyncio
import logging
import requests
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8318085474:AAGP7yS43M0vAe-3pQ-KQOdJbCJuNV_Mdxk"

# Логирование ошибок
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Города по умолчанию
CITIES = ["Astana", "Almaty", "London"]
user_city = {}
auto_update = {}

# --- Получение данных из API ---
def get_weather(city: str):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        local_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

        text = (
            f"🌆 Город: <b>{city}</b>\n"
            f"🌡 Температура: <b>{temp}°C</b>\n"
            f"☁️ Состояние: {desc}\n"
            f"🕒 Обновлено: {local_time}"
        )
        return text

    except requests.exceptions.Timeout:
        logging.error(f"⏱ Timeout при запросе к {city}")
        # Повторяем запрос один раз автоматически
        try:
            response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
            response.raise_for_status()
            data = response.json()
            temp = data["current_condition"][0]["temp_C"]
            desc = data["current_condition"][0]["weatherDesc"][0]["value"]
            local_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
            return (
                f"🌆 Город: <b>{city}</b>\n"
                f"🌡 Температура: <b>{temp}°C</b>\n"
                f"☁️ Состояние: {desc}\n"
                f"🕒 Обновлено (повтор): {local_time}"
            )
        except Exception as e:
            logging.error(f"Ошибка после повторного запроса: {e}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка API для {city}: {e}")
        return None

# --- Клавиатура основная ---
def get_keyboard(city: str, is_auto: bool):
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
            InlineKeyboardButton(text="🌆 Изменить город", callback_data="change_city")
        ],
        [
            InlineKeyboardButton(
                text=f"⏱ Автообновление: {'ВКЛ' if is_auto else 'ВЫКЛ'}",
                callback_data="toggle_auto"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- Клавиатура выбора города ---
def get_city_keyboard(current_city: str):
    buttons = []
    for c in CITIES:
        text = f"✅ {c}" if c == current_city else c
        buttons.append(InlineKeyboardButton(text=text, callback_data=f"set_city:{c}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

# --- Команда /start ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    city = "Astana"
    user_city[message.from_user.id] = city
    auto_update[message.from_user.id] = False

    weather = get_weather(city)
    if not weather:
        await message.answer("⚠️ API недоступно. Попробуйте позже.")
        return

    keyboard = get_keyboard(city, False)
    await message.answer(weather, reply_markup=keyboard, parse_mode="HTML")

# --- Обновление погоды ---
@dp.callback_query(F.data == "refresh")
async def refresh_weather(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city = user_city.get(user_id, "Astana")

    weather = get_weather(city)
    if not weather:
        await callback.answer("API недоступно…", show_alert=True)
        return

    keyboard = get_keyboard(city, auto_update[user_id])
    await callback.message.edit_text(weather, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("✅ Обновлено")

# --- Изменение города ---
@dp.callback_query(F.data == "change_city")
async def change_city(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_city = user_city.get(user_id, "Astana")

    city_keyboard = get_city_keyboard(current_city)
    await callback.message.edit_reply_markup(reply_markup=city_keyboard)
    await callback.answer()

# --- Выбор города ---
@dp.callback_query(F.data.startswith("set_city:"))
async def set_city(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    new_city = callback.data.split(":")[1]
    user_city[user_id] = new_city

    weather = get_weather(new_city)
    if not weather:
        await callback.answer("API недоступно…", show_alert=True)
        return

    keyboard = get_keyboard(new_city, auto_update[user_id])
    await callback.message.edit_text(weather, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(f"Город изменён на {new_city}")

# --- Автообновление ---
@dp.callback_query(F.data == "toggle_auto")
async def toggle_auto(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    auto_update[user_id] = not auto_update[user_id]
    city = user_city.get(user_id, "Astana")

    if auto_update[user_id]:
        await callback.answer("⏱ Автообновление включено!")
        asyncio.create_task(auto_refresh(callback.message, user_id))
    else:
        await callback.answer("⏹ Автообновление выключено!")

    keyboard = get_keyboard(city, auto_update[user_id])
    weather = get_weather(city)
    await callback.message.edit_text(weather, reply_markup=keyboard, parse_mode="HTML")

# --- Фоновое автообновление ---
async def auto_refresh(message: types.Message, user_id: int):
    while auto_update.get(user_id, False):
        await asyncio.sleep(30)
        city = user_city.get(user_id, "Astana")
        weather = get_weather(city)
        if weather:
            keyboard = get_keyboard(city, True)
            try:
                await message.edit_text(weather, reply_markup=keyboard, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Ошибка автообновления: {e}")
                break

# --- Запуск ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
