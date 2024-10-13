import hashlib
import hmac
import logging
import time
from urllib.parse import parse_qsl, unquote

from aiogram import Bot

from app.config import db_config, tgbot_config
from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.database.setup import create_engine, create_session_pool

engine = create_engine(db_config)
session_pool = create_session_pool(engine)
bot = Bot(tgbot_config.token)


async def get_repo():
    async with session_pool() as session:
        yield RequestsRepo(session)
