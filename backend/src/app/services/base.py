from app.infrastructure.database.repo.requests import RequestsRepo


class BaseService:
    """
    A class representing a base service for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the service.

    """

    def __init__(self, repo: RequestsRepo):
        self.repo: RequestsRepo = repo
