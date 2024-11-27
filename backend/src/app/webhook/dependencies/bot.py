from typing import AsyncGenerator

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from app.config import tgbot_config


async def get_bot() -> AsyncGenerator[Bot, None]:
    bot = Bot(token=tgbot_config.token, default=DefaultBotProperties(parse_mode="HTML"))
    try:
        yield bot
    finally:
        await bot.session.close()
