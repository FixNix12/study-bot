import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import load_config
from app.database import init_db
from app.scheduler import setup_scheduler
from app.services.ai_tutor_service import AiTutorService

from app.handlers.start import router as start_router
from app.handlers.lessons import router as lessons_router
from app.handlers.progress import router as progress_router
from app.handlers.ai_tutor import router as ai_tutor_router


async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    ai_tutor = AiTutorService(
        api_key=config.OPENAI_API_KEY,
        model=config.OPENAI_MODEL
    )

    dp["ai_tutor"] = ai_tutor

    dp.include_router(start_router)
    dp.include_router(lessons_router)
    dp.include_router(progress_router)
    dp.include_router(ai_tutor_router)

    await init_db()

    setup_scheduler(
        bot=bot,
        hour=config.DAILY_HOUR,
        minute=config.DAILY_MINUTE
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())