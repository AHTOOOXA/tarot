from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.services.requests import RequestsService
from app.config import rabbit_config

class ServiceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.producer = RabbitMQProducer(rabbit_config)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        repo = data.get("repo")
        if repo:
            service = RequestsService(repo, self.producer)
            data["service"] = service
            
        return await handler(event, data)
