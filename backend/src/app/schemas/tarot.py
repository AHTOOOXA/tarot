from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class SpreadType(str, Enum):
    SINGLE = "single"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"

class TarotCard(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    keywords: List[str]
    meaning_upright: str
    meaning_reversed: str
    is_reversed: bool = False

class TarotSpread(BaseModel):
    id: int
    name: str
    description: str
    num_cards: int
    positions: List[str]
    type: SpreadType

class TarotReading(BaseModel):
    id: int
    user_id: int
    spread_id: int
    cards: List[TarotCard]
    question: Optional[str]
    interpretation: str
    created_at: datetime
