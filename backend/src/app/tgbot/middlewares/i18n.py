from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.infrastructure.i18n import t
from app.schemas.users import UserSchema


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user: UserSchema = data.get("user")
        # Fallback to 'en' if no user or no language_code
        lang = user.language_code if user and user.language_code else "en"
        data["t"] = lambda key: t(key, lang)
        return await handler(event, data)
