from fastapi import Depends

from app.infrastructure.database.repo.requests import RequestsRepo
from app.webhook.dependencies.database import get_repo


class BaseService:
    """
    A class representing a base service for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the service.

    """

    def __init__(self, repo: RequestsRepo = Depends(get_repo)):
        self.repo: RequestsRepo = repo
