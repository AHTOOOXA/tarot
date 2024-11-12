from app.schemas.tarot import TarotReading, TarotCard
from datetime import datetime
from typing import List, Optional


class ReadingsRepo:
    _readings = []
    _next_id = 1

    async def create_reading(
        self,
        user_id: int,
        spread_id: int,
        cards: List[TarotCard],
        question: Optional[str],
        interpretation: str,
        created_at: datetime
    ) -> TarotReading:
        reading = TarotReading(
            id=self._next_id,
            user_id=user_id,
            spread_id=spread_id,
            cards=cards,
            question=question,
            interpretation=interpretation,
            created_at=created_at
        )
        self._readings.append(reading)
        self._next_id += 1
        return reading

    async def get_user_readings(self, user_id: int) -> List[TarotReading]:
        return [r for r in self._readings if r.user_id == user_id]
