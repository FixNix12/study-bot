import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    DAILY_HOUR: int
    DAILY_MINUTE: int


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set in .env")

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    return Config(
        BOT_TOKEN=bot_token,
        OPENAI_API_KEY=openai_api_key,
        OPENAI_MODEL=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        DAILY_HOUR=int(os.getenv("DAILY_HOUR", 10)),
        DAILY_MINUTE=int(os.getenv("DAILY_MINUTE", 0)),
    )