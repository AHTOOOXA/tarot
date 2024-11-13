from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.schemas.users import UserSchema
from app.services.requests import RequestsService


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        services: RequestsService = data.get("services")
        event_from_user = data.get("event_from_user")

        if not event_from_user:
            return await handler(event, data)

        user = await services.users.get_or_create_user(
            event_from_user.id, event_from_user.full_name, event_from_user.username
        )
        data["user"] = user

        return await handler(event, data)
