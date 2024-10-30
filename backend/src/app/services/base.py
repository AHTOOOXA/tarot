from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.requests import RequestsService

from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.webhook.dependencies.database import get_repo
from app.webhook.dependencies.rabbit import get_rabbit_producer


class BaseService:
    """
    A class representing a base service for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the service.

    """

    def __init__(
        self,
        repo: RequestsRepo,
        producer: RabbitMQProducer,
        services: "RequestsService",
    ):
        self.repo: RequestsRepo = repo
        self.producer: RabbitMQProducer = producer
        self.services: "RequestsService" = services
