from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import re
import os

# 🔹 Твой токен (не передавай его другим!)
TOKEN = "8492691594:AAHGomYK8lOc-AUGzJ-PtHGopAixKsPOlI0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция экранирования текста для MarkdownV2
def escape_markdown(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

# Функция безопасной отправки сообщений
async def send_safe_message(message: types.Message, text: str, reply_markup=None):
    safe_text = escape_markdown(text)
    await message.answer(safe_text, reply_markup=reply_markup, parse_mode="MarkdownV2")

# Главная клавиатура
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💰 Финансовая пирамида"),
                KeyboardButton(text="🎣 Фишинг"),
            ],
            [
                KeyboardButton(text="🏦 Финансовая безопасность"),
                KeyboardButton(text="👤 Кто такие дропы"),
            ],
            [
                KeyboardButton(text="📞 Контакты / Обратная связь"),
                KeyboardButton(text="ℹ️ Информация о боте"),
            ]
        ],
        resize_keyboard=True
    )

# Клавиатура для дропов с видео
def drops_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Посмотреть видео")],
            [KeyboardButton(text="⬅️ Назад в меню")]
        ],
        resize_keyboard=True
    )

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await send_safe_message(
        message,
        "Привет! 👋\nЯ бот-помощник от dias_helper.\nВыбери тему из меню или напиши /menu."
    )

# /menu
@dp.message(Command("menu"))
async def menu(message: types.Message):
    await send_safe_message(message, "Выбери интересующую тему 👇", reply_markup=main_menu())

# 💰 Финансовая пирамида
@dp.message(lambda message: message.text == "💰 Финансовая пирамида")
async def pyramid_info(message: types.Message):
    text = (
        "💰 *Финансовая пирамида* — это схема, где прибыль участников выплачивается не из реального бизнеса, "
        "а из вложений новых участников.\n\n"
        "🚫 Такие схемы незаконны и могут привести к потере денег.\n\n"
        "📌 *Признаки финансовой пирамиды:*\n"
        "• Обещание высокой доходности за короткий срок\n"
        "• Давление «вступить срочно»\n"
        "• Отсутствие прозрачного продукта или услуги"
    )
    await send_safe_message(message, text)

# 🎣 Фишинг
@dp.message(lambda message: message.text == "🎣 Фишинг")
async def phishing_info(message: types.Message):
    text = (
        "🎣 *Фишинг* — способ обмана, когда мошенники выдают себя за банки или сервисы, "
        "чтобы получить пароли и данные карт.\n\n"
        "⚠️ Никогда не переходи по подозрительным ссылкам!\n\n"
        "💡 *Советы для защиты:* \n"
        "• Не открывай письма от незнакомцев\n"
        "• Проверяй адреса сайтов\n"
        "• Используй двухфакторную аутентификацию"
    )
    await send_safe_message(message, text)

# 🏦 Финансовая безопасность
@dp.message(lambda message: message.text == "🏦 Финансовая безопасность")
async def safety_info(message: types.Message):
    text = (
        "🏦 *Финансовая безопасность* — это умение защищать свои деньги и личные данные от мошенников.\n\n"
        "✅ Советы:\n"
        "• Не передавай пароли и данные карт\n"
        "• Используй безопасные пароли и менеджеры паролей\n"
        "• Проверяй источники информации и банки"
    )
    await send_safe_message(message, text)

# 👤 Кто такие дропы (только текст + кнопки для видео)
@dp.message(lambda message: message.text == "👤 Кто такие дропы")
async def drops_info(message: types.Message):
    text = (
        "👤 *Дроп* (денежный мул) — человек, который за вознаграждение позволяет использовать "
        "свой банковский счёт для перевода чужих денег.\n\n"
        "⚠️ Это незаконно и может привести к уголовной ответственности.\n\n"
        "Нажми кнопку ниже, чтобы посмотреть короткое видео (30 секунд), как не стать дропом."
    )
    await send_safe_message(message, text, reply_markup=drops_menu())

# 🎬 Посмотреть видео
@dp.message(lambda message: message.text == "🎬 Посмотреть видео")
async def play_video(message: types.Message):
    text = (
        "🎬 *Как не стать дропом (30 секунд)*\n\n"
        "Смотри видео по ссылке: https://www.youtube.com/watch?v=fTJPyZyT5R8"
    )
    await send_safe_message(message, text)

# ⬅️ Назад в меню
@dp.message(lambda message: message.text == "⬅️ Назад в меню")
async def back_to_menu(message: types.Message):
    await send_safe_message(message, "Возврат в главное меню 👇", reply_markup=main_menu())

# 📞 Контакты / Обратная связь
@dp.message(lambda message: message.text == "📞 Контакты / Обратная связь")
async def contacts_info(message: types.Message):
    text = (
        "📞 Если у вас есть вопросы или предложения, пишите на почту: support@example.com\n"
        "💬 Также можете связаться через Telegram: @dias_helper_support"
    )
    await send_safe_message(message, text)

# ℹ️ Информация о боте
@dp.message(lambda message: message.text == "ℹ️ Информация о боте")
async def about_bot(message: types.Message):
    text = (
        "🤖 *Dias Helper Bot*\n"
        "Версия: 1.1\n"
        "Описание: Бот помогает узнать о финансовых рисках, фишинге, пирамидах и дропах.\n"
        "Создатель: dias_helper\n"
        "🛡️ Все советы даны в образовательных целях."
    )
    await send_safe_message(message, text)

# Запуск бота
async def main():
    print("✅ Бот запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
