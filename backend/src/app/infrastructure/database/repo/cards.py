from app.schemas.tarot import TarotCard

class CardsRepo:
    _cards = [
        {
            "id": 1,
            "name": "The Fool",
            "description": "New beginnings, innocence, spontaneity",
            "image_url": "https://www.sacred-texts.com/tarot/pkt/img/ar00.jpg",
            "keywords": ["beginnings", "innocence", "spontaneity", "free spirit"],
            "meaning_upright": "New beginnings, spontaneity, faith, apparent foolishness",
            "meaning_reversed": "Recklessness, risk-taking, bad decisions"
        },
        {
            "id": 2,
            "name": "The Magician",
            "description": "Manifestation, resourcefulness, power",
            "image_url": "https://www.sacred-texts.com/tarot/pkt/img/ar01.jpg",
            "keywords": ["power", "skill", "concentration", "action"],
            "meaning_upright": "Manifestation, resourcefulness, power, inspired action",
            "meaning_reversed": "Manipulation, poor planning, untapped talents"
        }
    ]

    async def get_random_card(self) -> TarotCard:
        import random
        card_data = random.choice(self._cards)
        return TarotCard(**card_data)
