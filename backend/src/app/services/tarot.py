import random
from datetime import datetime
from typing import List, Optional

import g4f

from app.infrastructure.i18n import i18n
from app.schemas.tarot import DailyReadingMessage, TarotCard
from app.schemas.users import UserSchema
from app.services.base import BaseService


class TarotService(BaseService):
    async def get_random_card(self) -> TarotCard:
        return await self.repo.cards.get_random_card()

    async def get_daily_reading(self, user: UserSchema) -> DailyReadingMessage:
        card = await self.get_random_card()

        prompt = i18n("gpt_prompts.daily_card").format(card_name=card.name, description=card.description)

        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            provider=g4f.Provider.Ai4Chat,
            messages=[{"role": "system", "content": i18n("gpt_prompts.system")}, {"role": "user", "content": prompt}],
        )

        return DailyReadingMessage(card=card, interpretation=response)

    async def get_question_reading(self, user: UserSchema, question: str) -> str:
        prompt = i18n("gpt_prompts.question_reading").format(question=question)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            provider=g4f.Provider.Ai4Chat,
            messages=[{"role": "system", "content": i18n("gpt_prompts.system")}, {"role": "user", "content": prompt}],
        )
        return response
