from dataclasses import dataclass

from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.services.inbox import InboxService
from app.services.quizzes import QuizzesService
from app.services.users import UserService


@dataclass
class RequestsService:
    """
    Services for handling database operations. This class holds all the services for the database models.

    You can add more services as properties to this class, so they will be easily accessible.
    """

    repo: RequestsRepo
    producer: RabbitMQProducer

    @property
    def quizzes(self) -> QuizzesService:
        return QuizzesService(self.repo, self.producer)

    @property
    def inbox(self) -> InboxService:
        return InboxService(self.repo, self.producer)

    @property
    def users(self) -> UserService:
        return UserService(self.repo, self.producer)
