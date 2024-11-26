import random
from typing import List

from app.schemas.tarot import TarotCard


class CardsRepo:
    _cards = [TarotCard(id=i, key=f"{i:02d}") for i in range(78)]

    async def get_random_card(self) -> TarotCard:
        return random.choice(self._cards)

    async def get_random_cards(self, count: int) -> List[TarotCard]:
        return random.sample(self._cards, count)
