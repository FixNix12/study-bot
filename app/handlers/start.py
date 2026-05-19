from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database import add_user


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(
        "Привет! Я твой учебный бот.\n\n"
        "Каждый день я буду присылать тебе материал по программированию.\n"
        "Ты сможешь отмечать темы как изученные, повторять их и проходить мини-тесты.\n\n"
        "Команды:\n"
        "/lesson — получить сегодняшний урок\n"
        "/progress — посмотреть прогресс"
    )