from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.infrastructure.i18n import i18n, t
from app.schemas.users import UserSchema


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        i18n.set_user_locale(data.get("user"))
        try:
            return await handler(event, data)
        finally:
            i18n.reset_translation()
