from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.lessons import LESSONS
from app.keyboards import lesson_keyboard, quiz_keyboard
from app.database import mark_lesson


router = Router()


def get_lesson_by_id(lesson_id: int):
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson

    return None


def get_daily_lesson():
    # MVP-логика: пока всегда первый урок.
    # Потом заменим на выбор следующего непройденного урока.
    return LESSONS[0]


def format_lesson(lesson: dict) -> str:
    return (
        f"📚 <b>{lesson['title']}</b>\n"
        f"Уровень: {lesson['level']}\n\n"
        f"{lesson['text']}\n\n"
        f"📝 <b>{lesson['task']}</b>"
    )


@router.message(Command("lesson"))
async def lesson_command(message: Message):
    lesson = get_daily_lesson()

    await message.answer(
        format_lesson(lesson),
        reply_markup=lesson_keyboard(lesson["id"]),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("lesson_completed:"))
async def lesson_completed_handler(callback: CallbackQuery):
    lesson_id = int(callback.data.split(":")[1])

    await mark_lesson(
        telegram_id=callback.from_user.id,
        lesson_id=lesson_id,
        status="completed"
    )

    await callback.answer("Урок отмечен как изученный ✅")

    await callback.message.answer(
        "Отлично. Материал закреплён.\n\n"
        "Завтра я пришлю следующую тему."
    )


@router.callback_query(F.data.startswith("lesson_repeat:"))
async def lesson_repeat_handler(callback: CallbackQuery):
    lesson_id = int(callback.data.split(":")[1])

    await mark_lesson(
        telegram_id=callback.from_user.id,
        lesson_id=lesson_id,
        status="repeat"
    )

    await callback.answer("Добавил в повторение 🔁")

    await callback.message.answer(
        "Хорошо, эту тему нужно будет повторить позже."
    )


@router.callback_query(F.data.startswith("lesson_quiz:"))
async def lesson_quiz_handler(callback: CallbackQuery):
    lesson_id = int(callback.data.split(":")[1])
    lesson = get_lesson_by_id(lesson_id)

    if not lesson:
        await callback.answer("Урок не найден")
        return

    quiz = lesson["quiz"]

    await callback.message.answer(
        f"🧠 <b>Мини-тест</b>\n\n{quiz['question']}",
        reply_markup=quiz_keyboard(lesson_id, quiz["options"]),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data.startswith("quiz_answer:"))
async def quiz_answer_handler(callback: CallbackQuery):
    _, lesson_id_raw, answer_raw = callback.data.split(":")

    lesson_id = int(lesson_id_raw)
    answer_index = int(answer_raw)

    lesson = get_lesson_by_id(lesson_id)

    if not lesson:
        await callback.answer("Урок не найден")
        return

    correct_index = lesson["quiz"]["correct"]

    if answer_index == correct_index:
        await callback.answer("Правильно ✅")
        await callback.message.answer("Верно. Тема понята хорошо.")
    else:
        await callback.answer("Неправильно ❌")
        await callback.message.answer(
            "Ответ неверный. Лучше перечитать объяснение и попробовать ещё раз."
        )