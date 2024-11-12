from app.schemas.tarot import SpreadType, TarotSpread

class SpreadsRepo:
    _spreads = {
        SpreadType.SINGLE: {
            "id": 1,
            "name": "Daily Card",
            "description": "A single card for daily guidance",
            "num_cards": 1,
            "positions": ["Daily Guidance"],
            "type": SpreadType.SINGLE
        },
        SpreadType.THREE_CARD: {
            "id": 2,
            "name": "Past-Present-Future",
            "description": "Three card spread showing situation progression",
            "num_cards": 3,
            "positions": ["Past", "Present", "Future"],
            "type": SpreadType.THREE_CARD
        }
    }

    async def get_spread_by_type(self, spread_type: SpreadType) -> TarotSpread:
        spread_data = self._spreads[spread_type]
        return TarotSpread(**spread_data)
