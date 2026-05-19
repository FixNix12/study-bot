import aiosqlite
from datetime import datetime


DB_PATH = "study_bot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                current_day INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                lesson_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                lesson_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                completed_at TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(telegram_id, lesson_id)
            )
        """)

        await db.commit()


async def add_user(telegram_id: int, username: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id, username, created_at)
            VALUES (?, ?, ?)
        """, (telegram_id, username, datetime.utcnow().isoformat()))

        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT telegram_id FROM users
        """)
        rows = await cursor.fetchall()

    return [row[0] for row in rows]


async def mark_lesson(telegram_id: int, lesson_id: int, status: str):
    completed_at = datetime.utcnow().isoformat() if status == "completed" else None

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_lessons (
                telegram_id,
                lesson_id,
                status,
                completed_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id, lesson_id)
            DO UPDATE SET
                status = excluded.status,
                completed_at = excluded.completed_at
        """, (
            telegram_id,
            lesson_id,
            status,
            completed_at,
            datetime.utcnow().isoformat()
        ))

        await db.commit()


async def get_completed_lessons_count(telegram_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM user_lessons
            WHERE telegram_id = ?
            AND status = 'completed'
        """, (telegram_id,))

        row = await cursor.fetchone()

    return row[0]


async def get_user_lesson_status(telegram_id: int, lesson_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT status
            FROM user_lessons
            WHERE telegram_id = ?
            AND lesson_id = ?
        """, (telegram_id, lesson_id))

        row = await cursor.fetchone()

    return row[0] if row else None


async def save_user_question(
    telegram_id: int,
    lesson_id: int | None,
    question: str,
    answer: str,
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_questions (
                telegram_id,
                lesson_id,
                question,
                answer,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            telegram_id,
            lesson_id,
            question,
            answer,
            datetime.utcnow().isoformat()
        ))

        await db.commit()