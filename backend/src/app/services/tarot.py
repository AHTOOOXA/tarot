from typing import List, Optional
from datetime import datetime
import g4f
import random

from app.services.base import BaseService
from app.schemas.tarot import (
    TarotSpread,
    TarotCard,
    TarotReading,
    SpreadType
)

class TarotService(BaseService):
    async def get_random_card(self) -> TarotCard:
        return await self.repo.cards.get_random_card()
    
    async def generate_interpretation(
        self,
        spread: TarotSpread,
        cards: List[TarotCard],
        question: Optional[str]
    ) -> str:
        prompt = self._build_interpretation_prompt(spread, cards, question)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            provider=g4f.Provider.Ai4Chat,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response
    
    def _build_interpretation_prompt(
        self,
        spread: TarotSpread,
        cards: List[TarotCard],
        question: Optional[str]
    ) -> str:
        prompt = f"Interpret this {spread.name} tarot spread:\n\n"
        
        if question:
            prompt += f"Question: {question}\n\n"
            
        for position, card in zip(spread.positions, cards):
            orientation = "reversed" if card.is_reversed else "upright"
            prompt += f"{position}: {card.name} ({orientation})\n"
            prompt += f"Keywords: {', '.join(card.keywords)}\n"
            meaning = card.meaning_reversed if card.is_reversed else card.meaning_upright
            prompt += f"Meaning: {meaning}\n\n"
            
        prompt += "\nProvide a detailed interpretation of how these cards interact and answer the question (if provided)."
        return prompt

    async def create_reading(
        self,
        user_id: int,
        spread_type: SpreadType,
        question: Optional[str] = None
    ) -> TarotReading:
        spread = await self.repo.spreads.get_spread_by_type(spread_type)
        cards = []
        
        for _ in range(spread.num_cards):
            card = await self.get_random_card()
            card.is_reversed = bool(random.getrandbits(1))
            cards.append(card)
            
        interpretation = await self.generate_interpretation(spread, cards, question)
            
        reading = await self.repo.readings.create_reading(
            user_id=user_id,
            spread_id=spread.id,
            cards=cards,
            question=question,
            interpretation=interpretation,
            created_at=datetime.utcnow()
        )
        
        return reading
