from pydantic import BaseModel, computed_field

from app.config import tgbot_config
from app.infrastructure.i18n import i18n


class TarotCard(BaseModel):
    id: int
    key: str

    @computed_field
    @property
    def name(self) -> str:
        return i18n(f"cards.{self.key}.name")

    @computed_field
    @property
    def description(self) -> str:
        return i18n(f"cards.{self.key}.description")

    @computed_field
    @property
    def image_url(self) -> str:
        return f"images/moon_magic_tarot/{self.key}.jpg"


class DailyReadingMessage(BaseModel):
    card: TarotCard
    interpretation: str
