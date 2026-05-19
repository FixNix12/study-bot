from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states import AskAiState
from app.services.lesson_service import get_lesson_by_id
from app.database import save_user_question


router = Router()


def split_long_message(text: str, max_length: int = 3900) -> list[str]:
    parts = []

    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)

        if split_index == -1:
            split_index = max_length

        parts.append(text[:split_index])
        text = text[split_index:].strip()

    if text:
        parts.append(text)

    return parts


@router.message(Command("ask"))
async def ask_command(message: Message, ai_tutor):
    question = message.text.replace("/ask", "", 1).strip()

    if not question:
        await message.answer(
            "Напиши вопрос после команды.\n\n"
            "Пример:\n"
            "/ask Объясни замыкания простыми словами"
        )
        return

    await message.answer("Думаю над ответом 🤖")

    answer = await ai_tutor.answer_question(
        question=question,
        lesson=None
    )

    await save_user_question(
        telegram_id=message.from_user.id,
        lesson_id=None,
        question=question,
        answer=answer
    )

    for part in split_long_message(answer):
        await message.answer(part)


@router.callback_query(F.data.startswith("ask_ai:"))
async def ask_ai_callback(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split(":")[1])

    await state.set_state(AskAiState.waiting_for_question)
    await state.update_data(lesson_id=lesson_id)

    lesson = get_lesson_by_id(lesson_id)

    await callback.message.answer(
        "🤖 Напиши вопрос по текущей теме.\n\n"
        f"Тема: {lesson['title'] if lesson else 'урок'}\n\n"
        "Например:\n"
        "— объясни проще\n"
        "— почему здесь this теряется?\n"
        "— дай ещё один пример\n"
        "— проверь мой ответ"
    )

    await callback.answer()


@router.message(AskAiState.waiting_for_question)
async def ai_question_message(message: Message, state: FSMContext, ai_tutor):
    data = await state.get_data()
    lesson_id = data.get("lesson_id")

    lesson = get_lesson_by_id(lesson_id) if lesson_id else None
    question = message.text

    await message.answer("Разбираю вопрос 🤖")

    answer = await ai_tutor.answer_question(
        question=question,
        lesson=lesson
    )

    await save_user_question(
        telegram_id=message.from_user.id,
        lesson_id=lesson_id,
        question=question,
        answer=answer
    )

    for part in split_long_message(answer):
        await message.answer(part)

    await state.clear()