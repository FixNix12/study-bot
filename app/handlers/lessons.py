from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.keyboards import lesson_keyboard, quiz_keyboard
from app.database import mark_lesson
from app.services.lesson_service import get_lesson_by_id, get_next_lesson_for_user


router = Router()


def format_lesson(lesson: dict) -> str:
    return (
        f"📚 <b>День {lesson['day']}</b>\n"
        f"🧩 <b>Модуль:</b> {lesson['module']}\n"
        f"🎯 <b>Тема:</b> {lesson['title']}\n\n"
        f"📖 <b>Теория:</b>\n{lesson['theory']}\n\n"
        f"💻 <b>Пример кода:</b>\n"
        f"<pre><code>{lesson['code']}</code></pre>\n\n"
        f"📝 <b>Задание:</b>\n{lesson['task']}"
    )


@router.message(Command("lesson"))
async def lesson_command(message: Message):
    lesson = await get_next_lesson_for_user(message.from_user.id)

    if not lesson:
        await message.answer(
            "🎉 Ты прошёл всю программу обучения!\n\n"
            "Теперь можно переходить к финальному full-stack проекту."
        )
        return

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

    next_lesson = await get_next_lesson_for_user(callback.from_user.id)

    if not next_lesson:
        await callback.message.answer(
            "🎉 Отлично! Ты прошёл все доступные уроки.\n\n"
            "Когда добавим новые уроки — бот продолжит обучение."
        )
        return

    await callback.message.answer(
        "Отлично. Материал закреплён ✅\n\n"
        "Следующий урок будет доступен по команде /lesson "
        "или придёт автоматически по расписанию."
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

    quiz = lesson.get("quiz")

    if not quiz:
        await callback.answer("Для этого урока пока нет теста")
        await callback.message.answer(
            "Для этого урока пока нет мини-теста. "
            "Можешь закрепить тему через задание или задать вопрос AI-наставнику."
        )
        return

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

    quiz = lesson.get("quiz")

    if not quiz:
        await callback.answer("Тест не найден")
        return

    correct_index = quiz["correct"]

    if answer_index == correct_index:
        await callback.answer("Правильно ✅")
        await callback.message.answer("Верно. Тема понята хорошо.")
    else:
        correct_answer = quiz["options"][correct_index]

        await callback.answer("Неправильно ❌")
        await callback.message.answer(
            "Ответ неверный.\n\n"
            f"Правильный ответ: <b>{correct_answer}</b>\n\n"
            "Лучше перечитать объяснение и попробовать применить тему в коде.",
            parse_mode="HTML"
        )