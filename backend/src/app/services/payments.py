import uuid

from yookassa import Configuration, Payment

from app.config import yookassa_config


class PaymentsService:
    def __init__(self):
        Configuration.account_id = yookassa_config.shop_id
        Configuration.secret_key = yookassa_config.secret_key

    async def create_payment(self, amount: float, currency: str, description: str, return_url: str):
        payment = Payment.create(
            {
                "amount": {"value": amount, "currency": currency},
                "confirmation": {"type": "redirect", "return_url": return_url},
                "capture": True,
                "description": description,
            },
            uuid.uuid4(),
        )
        return payment.confirmation.confirmation_url
