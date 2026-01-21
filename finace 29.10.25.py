from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import re

# 🔹 Токен
TOKEN = "8492691594:AAGx96Aqi9jdNW0SLhe6Hg9X_iikLLCK91s"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ---------- Экранирование MarkdownV2 ----------
def escape_markdown(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


async def send_safe_message(chat_id, text: str, reply_markup=None):
    safe_text = escape_markdown(text)
    await bot.send_message(chat_id, safe_text, reply_markup=reply_markup, parse_mode="MarkdownV2")


# ---------- Главное меню Inline ----------
def main_menu_inline() -> InlineKeyboardMarkup:
    keyboard_rows = [
        [InlineKeyboardButton(text="💰 Финансовая пирамида", callback_data="pyramid")],
        [InlineKeyboardButton(text="🎣 Фишинг", callback_data="phishing")],
        [InlineKeyboardButton(text="🏦 Финансовая безопасность", callback_data="safety")],
        [InlineKeyboardButton(text="👤 Кто такие дропы", callback_data="drops")],
        [InlineKeyboardButton(text="🧩 Викторина", callback_data="quiz")],
        [InlineKeyboardButton(text="📞 Контакты / Обратная связь", callback_data="contacts")],
        [InlineKeyboardButton(text="ℹ️ Информация о боте", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


# ---------- Викторина Inline ----------
QUIZ = [
    {
        "question": "1️⃣ Что такое финансовая пирамида?",
        "options": {
            "A": "Стабильный инвестиционный фонд",
            "B": "Схема, где прибыль выплачивается из вкладов новых участников",
            "C": "Легальный банковский вклад"
        },
        "correct": "B"
    },
    {
        "question": "2️⃣ Что делать при подозрительном сообщении от 'банка'?",
        "options": {
            "A": "Перейти по ссылке",
            "B": "Ввести свои данные",
            "C": "Не переходить и проверить в официальном приложении"
        },
        "correct": "C"
    }
]


def quiz_keyboard(options: dict) -> InlineKeyboardMarkup:
    # Создаем список рядов кнопок
    keyboard_rows = []
    for key, val in options.items():
        button = InlineKeyboardButton(text=f"{key}) {val}", callback_data=key)
        keyboard_rows.append([button])  # каждая кнопка в отдельном ряду
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


# ---------- Хранилище прогресса викторины ----------
user_quiz_state = {}  # {user_id: {"index": 0, "score": 0, "last_msg_id": int}}


# ---------- Основные команды ----------
@dp.message(Command("start"))
async def start(message: types.Message):
    await send_safe_message(message.chat.id,
                            "Привет! 👋\nЯ бот-помощник от dias_helper.\nВыбери тему из меню.",
                            reply_markup=main_menu_inline())


# ---------- Обработка всех нажатий кнопок ----------
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    # Сразу скрываем главное меню
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass  # если сообщение нельзя редактировать

    # ---------- Информационные разделы ----------
    if data == "pyramid":
        text = (
            "💰 *Финансовая пирамида* — это схема, где прибыль участников выплачивается из вкладов новых участников.\n\n"
            "🚫 Такие схемы незаконны и могут привести к потере денег.\n\n"
            "📌 *Признаки финансовой пирамиды:*\n"
            "• Обещание высокой доходности за короткий срок\n"
            "• Давление «вступить срочно»\n"
            "• Отсутствие прозрачного продукта или услуги"
        )
        await send_safe_message(callback.message.chat.id, text)

    elif data == "phishing":
        text = (
            "🎣 *Фишинг* — способ обмана, когда мошенники выдают себя за банки или сервисы, "
            "чтобы получить пароли и данные карт.\n\n"
            "⚠️ Никогда не переходи по подозрительным ссылкам!\n\n"
            "💡 *Советы для защиты:* \n"
            "• Не открывай письма от незнакомцев\n"
            "• Проверяй адреса сайтов\n"
            "• Используй двухфакторную аутентификацию"
        )
        await send_safe_message(callback.message.chat.id, text)

    elif data == "safety":
        text = (
            "🏦 *Финансовая безопасность* — это умение защищать свои деньги и личные данные от мошенников.\n\n"
            "✅ Советы:\n"
            "• Не передавай пароли и данные карт\n"
            "• Используй безопасные пароли и менеджеры паролей\n"
            "• Проверяй источники информации и банки"
        )
        await send_safe_message(callback.message.chat.id, text)

    elif data == "drops":
        text = (
            "👤 *Дроп* (денежный мул) — человек, который за вознаграждение позволяет использовать "
            "свой банковский счёт для перевода чужих денег.\n\n⚠️ Это незаконно и может привести к уголовной ответственности.\n\n"
            "Смотри видео: https://www.youtube.com/watch?v=fTJPyZyT5R8"
        )
        await send_safe_message(callback.message.chat.id, text)


    elif data == "contacts":

        text = (

            "📞 Вопросы и предложения: @quinxray\n"

            "💬 Поддержка: @dias_helper_support\n\n"

            "⚠️ Экстренные ситуации (Полиция: 102):\n"

            "Актюбинской области: kense.dp.aktobe@mvd.gov.kz:\n"

            "г. Астаны: polise.astana@mvd.gov.kz:\n"

            "Департамент полиции на транспорте: o.kantselyariya@mvd.gov.kz:\n"

            "Адрес для общей переписки: Электронный адрес kense@mvd.gov.kz:\n"

            "• Email: info@police.kz"

        )

        await send_safe_message(callback.message.chat.id, text)


    elif data == "about":

        text = "🤖 *Dias Helper Bot*\nВерсия: 1.2\nОписание: Обучает финансовой грамотности и безопасности.\nСоздатель: dias_helper"

        await send_safe_message(callback.message.chat.id, text)


    # ---------- Викторина ----------
    elif data == "quiz":
        user_quiz_state[user_id] = {"index": 0, "score": 0, "last_msg_id": None}
        question = QUIZ[0]
        msg = await callback.message.answer(question["question"], reply_markup=quiz_keyboard(question["options"]))
        user_quiz_state[user_id]["last_msg_id"] = msg.message_id

    # ---------- Обработка ответов на вопросы викторины ----------
    elif user_id in user_quiz_state:
        state = user_quiz_state[user_id]
        current_index = state["index"]
        question = QUIZ[current_index]

        # Удаляем предыдущие кнопки
        if state.get("last_msg_id"):
            try:
                await bot.delete_message(callback.message.chat.id, state["last_msg_id"])
            except:
                pass

        # Проверка ответа
        if data == question["correct"]:
            state["score"] += 1
            await send_safe_message(callback.message.chat.id, "✅ Правильно!")
        else:
            correct_text = question["options"][question["correct"]]
            await send_safe_message(callback.message.chat.id, f"❌ Неправильно.\nПравильный ответ: {correct_text}")

        state["index"] += 1

        # Следующий вопрос или завершение
        if state["index"] < len(QUIZ):
            next_q = QUIZ[state["index"]]
            msg = await callback.message.answer(next_q["question"], reply_markup=quiz_keyboard(next_q["options"]))
            state["last_msg_id"] = msg.message_id
        else:
            score = state["score"]
            total = len(QUIZ)
            del user_quiz_state[user_id]
            # Меню возвращается только после окончания викторины
            await send_safe_message(callback.message.chat.id,
                                    f"🎉 Викторина окончена!\nТы набрал {score} из {total} правильных ответов!",
                                    reply_markup=main_menu_inline())


# ---------- Запуск ----------
async def main():
    print("✅ Бот запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
