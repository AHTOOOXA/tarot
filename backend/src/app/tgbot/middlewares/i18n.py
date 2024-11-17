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
        user: UserSchema = data.get("user")

        lang = "en"
        if user:
            if user.app_language_code:
                lang = user.app_language_code
            elif user.language_code:
                lang = user.language_code

        # Set translation for this request
        i18n.set_translation(lambda key: t(key, lang))

        try:
            return await handler(event, data)
        finally:
            # Clean up after request
            i18n.reset_translation()
