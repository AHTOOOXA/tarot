from typing import List

from pydantic import BaseModel

from app.config import tgbot_config


class TarotCard(BaseModel):
    id: int
    key: str

    @property
    def name(self) -> str:
        from app.infrastructure.i18n import i18n

        return i18n(f"cards.{self.key}.name")

    @property
    def description(self) -> str:
        from app.infrastructure.i18n import i18n

        return i18n(f"cards.{self.key}.description")

    @property
    def image_url(self) -> str:
        return f"{tgbot_config.api_domain}/static/images/moon_magic_tarot/{self.key}.jpg"


class DailyReadingMessage(BaseModel):
    card: TarotCard
    interpretation: str
