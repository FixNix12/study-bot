from openai import AsyncOpenAI


class AiTutorService:
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def answer_question(
        self,
        question: str,
        lesson: dict | None = None,
    ) -> str:
        lesson_context = ""

        if lesson:
            lesson_context = f"""
Текущий урок пользователя:
Модуль: {lesson.get("module")}
День: {lesson.get("day")}
Тема: {lesson.get("title")}

Теория урока:
{lesson.get("theory")}

Пример кода:
{lesson.get("code")}

Задание:
{lesson.get("task")}
"""

        system_prompt = f"""
Ты — личный AI-наставник по программированию для пользователя.

Пользователь изучает:
- JavaScript Core
- TypeScript
- NestJS
- PostgreSQL
- Redis
- Next.js
- Архитектуру больших проектов
- Микросервисы
- Python FastAPI
- React Native
- Docker
- Tests

Стиль ответа:
- отвечай на русском;
- объясняй простыми словами;
- сначала дай короткую суть;
- потом пример кода, если он помогает;
- не перегружай теорией;
- связывай объяснение с реальными backend/frontend задачами;
- если вопрос связан с ошибкой в коде, объясни причину и покажи исправление;
- если пользователь просит готовый ответ к заданию, помоги, но объясни логику.

{lesson_context}
"""

        response = await self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        return response.output_text