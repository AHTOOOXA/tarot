import random
from datetime import datetime
from typing import List, Optional

import g4f

from app.schemas.tarot import DailyReadingMessage, TarotCard
from app.schemas.users import UserSchema
from app.services.base import BaseService


class TarotService(BaseService):
    async def get_random_card(self) -> TarotCard:
        return await self.repo.cards.get_random_card()

    async def get_daily_reading(self, user: UserSchema) -> DailyReadingMessage:
        card = await self.get_random_card()
        prompt = f"Interpret this {card.name} tarot card:\n\n{card.description} as daily tarot reading. Interpretation should be in 100 words or less."
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4, provider=g4f.Provider.Ai4Chat, messages=[{"role": "user", "content": prompt}]
        )
        reading = DailyReadingMessage(card=card, interpretation=response)
        return reading
