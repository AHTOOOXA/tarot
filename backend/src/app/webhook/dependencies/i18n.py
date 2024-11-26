from typing import AsyncGenerator

from fastapi import Depends, Request

from app.infrastructure.i18n import I18nManager, i18n
from app.schemas.users import UserSchema
from app.webhook.auth import get_twa_user


async def get_i18n(request: Request, user: UserSchema = Depends(get_twa_user)) -> AsyncGenerator[I18nManager, None]:
    i18n.set_user_locale(user)
    try:
        yield i18n
    finally:
        i18n.reset_translation()
