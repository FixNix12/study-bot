from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.lessons import LESSONS
from app.database import get_completed_lessons_count


router = Router()


async def get_progress_text(telegram_id: int) -> str:
    completed = await get_completed_lessons_count(telegram_id)
    total = len(LESSONS)

    percent = round((completed / total) * 100) if total else 0

    return (
        "📊 <b>Твой прогресс</b>\n\n"
        f"Пройдено уроков: {completed}/{total}\n"
        f"Прогресс: {percent}%"
    )


@router.message(Command("progress"))
async def progress_command(message: Message):
    text = await get_progress_text(message.from_user.id)

    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "progress")
async def progress_callback(callback: CallbackQuery):
    text = await get_progress_text(callback.from_user.id)

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()