def analyze_text(text):
    """Анализирует текст: длину, количество слов и букв 'а'."""
    length = len(text)
    words = len(text.split())
    count_a = text.lower().count('а')
    return f"Длина: {length}\nСлов: {words}\nБукв 'а': {count_a}"


def create_message(user, topic):
    """Создает приветственное сообщение с использованием f-строки."""
    return f"Привет, {user}! Сегодня мы изучаем {topic}."


def format_news(title, body):
    """Форматирует новостной пост для бота."""
    title_upper = title.upper()
    body_replaced = body.replace("!", "🔥")
    if len(body_replaced) > 100:
        body_replaced = body_replaced[:100] + "..."
    return f"{title_upper}\n\n{body_replaced}"


# --- Примеры проверки ---
if __name__ == "__main__":
    print(analyze_text("Dias учится в колледже"))
    print()
    print(create_message("Dias", "функ  ции Python"))
    print()
    print(format_news("важная новость", "Сегодня отличный день! Учимся писать код и делаем успехи!"))
