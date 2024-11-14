from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repo.cards import CardsRepo
from app.infrastructure.database.repo.groups import GroupRepo
from app.infrastructure.database.repo.readings import ReadingsRepo
from app.infrastructure.database.repo.users import UserRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.session)

    @property
    def groups(self) -> GroupRepo:
        return GroupRepo(self.session)

    @property
    def cards(self) -> CardsRepo:
        return CardsRepo()

    @property
    def readings(self) -> ReadingsRepo:
        return ReadingsRepo()
