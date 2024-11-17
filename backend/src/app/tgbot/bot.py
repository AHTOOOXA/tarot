from app.infrastructure.logging import setup_logging

setup_logging()

import asyncio
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from app.config import db_config, rabbit_config, redis_config, tgbot_config
from app.infrastructure.database.setup import create_engine, create_session_pool
from app.infrastructure.logging import get_logger
from app.infrastructure.rabbit.consumer import RabbitMQConsumer
from app.tgbot.handlers import routers_list
from app.tgbot.middlewares.auth import AuthMiddleware
from app.tgbot.middlewares.database import DatabaseMiddleware
from app.tgbot.middlewares.i18n import I18nMiddleware
from app.tgbot.middlewares.service import ServiceMiddleware
from app.tgbot.services import broadcaster

logger = get_logger(__name__)


async def on_startup(bot: Bot, admin_ids: List[int]):
    await broadcaster.broadcast(bot, admin_ids, "Bot has been started")


async def process_rabbitmq_message(bot: Bot, data: dict):
    user_id, text = data.get("user_id"), data.get("text")
    if user_id and text:
        await broadcaster.send_message(bot, user_id, text)


async def start_consumer(consumer: RabbitMQConsumer, bot: Bot):
    await consumer.start_consuming(process_rabbitmq_message, bot)


async def main():
    logger.info("Starting bot")

    bot = Bot(token=tgbot_config.token, default=DefaultBotProperties(parse_mode="HTML"))
    storage = RedisStorage.from_url(
        redis_config.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )
    consumer = RabbitMQConsumer(rabbit_config)
    dp = Dispatcher(storage=storage)

    engine = create_engine(db_config)
    session_pool = create_session_pool(engine)
    dp.update.outer_middleware(DatabaseMiddleware(session_pool))
    dp.update.outer_middleware(ServiceMiddleware())
    dp.update.outer_middleware(AuthMiddleware())
    dp.update.outer_middleware(I18nMiddleware())
    dp.include_routers(*routers_list)

    await on_startup(bot, tgbot_config.admin_ids)

    try:
        logger.info("Starting consumer")
        consumer_task = asyncio.create_task(start_consumer(consumer, bot))

        logger.info("Starting polling")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        logger.info("Shutting down")
        await consumer.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has been stopped")
