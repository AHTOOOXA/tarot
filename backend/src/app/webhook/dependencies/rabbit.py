from app.config import rabbit_config
from app.infrastructure.rabbit.producer import RabbitMQProducer


async def get_rabbit_producer():
    return RabbitMQProducer(rabbit_config)
