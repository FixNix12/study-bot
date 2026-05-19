from app.curriculum import CURRICULUM
from app.database import get_user_lesson_status


def get_lesson_by_id(lesson_id: int):
    for lesson in CURRICULUM:
        if lesson["id"] == lesson_id:
            return lesson

    return None


async def get_next_lesson_for_user(telegram_id: int):
    for lesson in CURRICULUM:
        status = await get_user_lesson_status(
            telegram_id=telegram_id,
            lesson_id=lesson["id"]
        )

        if status != "completed":
            return lesson

    return None