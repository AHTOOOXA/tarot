from fastapi import Depends

from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.services.requests import RequestsService
from app.webhook.dependencies.database import get_repo
from app.webhook.dependencies.rabbit import get_rabbit_producer


async def get_services(
    repo: RequestsRepo = Depends(get_repo), producer: RabbitMQProducer = Depends(get_rabbit_producer)
):
    yield RequestsService(repo, producer)
