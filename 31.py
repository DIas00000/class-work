from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio

BOT_TOKEN = "8492691594:AAHGomYK8lOc-AUGzJ-PtHGopAixKsPOlI0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ---------- 1️⃣ Описание состояний ----------
class FoodForm(StatesGroup):
    name = State()
    dish = State()
    rating = State()


# ---------- 2️⃣ Команда /start ----------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! это dias helper.\n\n"
        "Начни сценарий командой /food 🍽️\n"
        "Или останови его в любой момент с помощью /cancel."
    )


# ---------- 3️⃣ Команда /food ----------
@dp.message(Command("food"))
async def cmd_food(message: types.Message, state: FSMContext):
    await state.set_state(FoodForm.name)
    await message.answer("Как тебя зовут?")


# ---------- 4️⃣ Ввод имени ----------
@dp.message(FoodForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FoodForm.dish)
    await message.answer("Отлично! Какое твое любимое блюдо?")


# ---------- 5️⃣ Ввод блюда ----------
@dp.message(FoodForm.dish)
async def process_dish(message: types.Message, state: FSMContext):
    await state.update_data(dish=message.text)
    await state.set_state(FoodForm.rating)
    await message.answer("Оцени его от 1 до 10 ⭐")


# ---------- 6️⃣ Ввод оценки ----------
@dp.message(FoodForm.rating)
async def process_rating(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Введите число от 1 до 10 🔢")
        return

    await state.update_data(rating=int(message.text))
    data = await state.get_data()

    name = data["name"]
    dish = data["dish"]
    rating = data["rating"]

    await message.answer(
        f"Спасибо, {name}! 🙌\n"
        f"Твое любимое блюдо — {dish}, оценка: {rating}/10 ⭐"
    )

    await state.clear()


# ---------- 7️⃣ Команда /cancel ----------
@dp.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Сценарий отменён. ❌")


# ---------- 8️⃣ Запуск ----------
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
