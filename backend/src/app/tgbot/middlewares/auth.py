from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update

from app.schemas.users import UserSchema
from app.services.requests import RequestsService


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery | Update, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | Update,
        data: Dict[str, Any],
    ) -> Any:
        services: RequestsService = data.get("services")

        # Extract Telegram user based on event type
        if isinstance(event, Message):
            tg_user = event.from_user
        elif isinstance(event, CallbackQuery):
            tg_user = event.from_user
        else:
            # For other update types, try to get from event_from_user
            tg_user = data.get("event_from_user")

        if not tg_user:
            return await handler(event, data)

        user_data = UserSchema(
            user_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            language_code=tg_user.language_code,
            is_bot=tg_user.is_bot,
            is_premium=tg_user.is_premium,
        )

        user = await services.users.get_or_create_user(user_data)
        data["user"] = user

        return await handler(event, data)
