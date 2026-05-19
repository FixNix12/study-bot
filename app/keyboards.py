from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def lesson_keyboard(lesson_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Изучил",
                    callback_data=f"lesson_completed:{lesson_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔁 Повторить позже",
                    callback_data=f"lesson_repeat:{lesson_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Мини-тест",
                    callback_data=f"lesson_quiz:{lesson_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🤖 Спросить AI-наставника",
                    callback_data=f"ask_ai:{lesson_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Мой прогресс",
                    callback_data="progress"
                )
            ]
        ]
    )


def quiz_keyboard(lesson_id: int, options: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for index, option in enumerate(options):
        buttons.append([
            InlineKeyboardButton(
                text=option,
                callback_data=f"quiz_answer:{lesson_id}:{index}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)