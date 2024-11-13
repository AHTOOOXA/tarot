from typing import List

from pydantic import BaseModel


class TarotCard(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    keywords: List[str]
    meaning_upright: str
    meaning_reversed: str
    is_reversed: bool = False


class DailyReadingMessage(BaseModel):
    card: TarotCard
    interpretation: str
