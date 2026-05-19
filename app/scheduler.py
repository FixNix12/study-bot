from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import get_all_users
from app.keyboards import lesson_keyboard
from app.services.lesson_service import get_next_lesson_for_user


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


async def send_daily_lessons(bot: Bot):
    users = await get_all_users()

    for telegram_id in users:
        try:
            lesson = await get_next_lesson_for_user(telegram_id)

            if not lesson:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=(
                        "🎉 Ты прошёл все доступные уроки.\n\n"
                        "Когда появятся новые материалы, я продолжу обучение."
                    )
                )
                continue

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