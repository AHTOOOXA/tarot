import logging

import g4f

from app.infrastructure.i18n import i18n
from app.schemas.tarot import DailyReadingMessage, TarotCard
from app.schemas.users import UserSchema
from app.services.base import BaseService

logger = logging.getLogger(__name__)


class TarotService(BaseService):
    async def get_random_card(self) -> TarotCard:
        return await self.repo.cards.get_random_card()

    async def get_daily_reading(self, user: UserSchema, card: TarotCard) -> DailyReadingMessage:
        system_prompt = i18n("gpt_prompts.system")
        daily_prompt = i18n("gpt_prompts.daily_card").format(card_name=card.name, description=card.description)
        prompt = f"{system_prompt}\n\n{daily_prompt}"

        logger.info(f"System prompt: {system_prompt}")
        logger.info(f"Daily prompt: {daily_prompt}")
        logger.info(f"Combined prompt: {prompt}")

        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4_turbo,
            provider=g4f.Provider.Airforce,
            messages=[{"role": "system", "content": prompt}],
        )

        return DailyReadingMessage(card=card, interpretation=response)

    async def get_question_reading(self, user: UserSchema, question: str) -> str:
        prompt = i18n("gpt_prompts.question_reading").format(question=question)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4_turbo,
            provider=g4f.Provider.Airforce,
            messages=[
                {"role": "system", "content": i18n("gpt_prompts.system") + i18n("gpt_prompts.question_reading")},
                {"role": "user", "content": prompt},
            ],
        )
        return response
