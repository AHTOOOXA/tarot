from dataclasses import dataclass

from app.infrastructure.database.repo.requests import RequestsRepo
from app.services.inbox import InboxService
from app.services.quizzes import QuizzesService


@dataclass
class RequestsService:
    """
    Services for handling database operations. This class holds all the services for the database models.

    You can add more services as properties to this class, so they will be easily accessible.
    """

    repo: RequestsRepo

    @property
    def quizzes(self) -> QuizzesService:
        return QuizzesService(self.repo)

    @property
    def inbox(self) -> InboxService:
        return InboxService(self.repo)
