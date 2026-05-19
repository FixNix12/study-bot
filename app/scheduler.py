from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import get_all_users
from app.lessons import LESSONS
from app.keyboards import lesson_keyboard


def format_lesson(lesson: dict) -> str:
    return (
        f"📚 <b>{lesson['title']}</b>\n"
        f"Уровень: {lesson['level']}\n\n"
        f"{lesson['text']}\n\n"
        f"📝 <b>{lesson['task']}</b>"
    )


def get_daily_lesson():
    # Пока MVP: первый урок.
    # Следующим шагом сделаем выдачу следующего непройденного урока.
    return LESSONS[0]


async def send_daily_lessons(bot: Bot):
    users = await get_all_users()
    lesson = get_daily_lesson()

    for telegram_id in users:
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=format_lesson(lesson),
                reply_markup=lesson_keyboard(lesson["id"]),
                parse_mode="HTML"
            )
        except Exception as error:
            print(f"Failed to send lesson to {telegram_id}: {error}")


def setup_scheduler(bot: Bot, hour: int, minute: int):
    scheduler = AsyncIOScheduler(timezone="Europe/Prague")

    scheduler.add_job(
        send_daily_lessons,
        trigger="cron",
        hour=hour,
        minute=minute,
        args=[bot],
        id="daily_lessons",
        replace_existing=True
    )

    scheduler.start()

    return scheduler