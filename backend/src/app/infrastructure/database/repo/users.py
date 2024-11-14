from typing import Optional

from sqlalchemy import and_, or_, select, update
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.database.models import Friendship, User
from app.infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(self, user_data: dict) -> User:
        """
        Creates or updates a user in the database and returns the user object.
        :param dict user_data: User data.
        :return: User object, None if there was an error while making a transaction.
        """

        # filter out None values to let DB defaults work
        filtered_data = {k: v for k, v in user_data.items() if v is not None}

        insert_stmt = (
            insert(User)
            .values(**filtered_data)
            .on_conflict_do_update(index_elements=[User.user_id], set_=filtered_data)
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def update_user(self, user_id: int, user_data: dict):
        stmt = update(User).where(User.user_id == user_id).values(**user_data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_friendship(self, user_id1: int, user_id2: int) -> Optional[Friendship]:
        stmt = select(Friendship).where(
            or_(
                and_(Friendship.user_id1 == user_id1, Friendship.user_id2 == user_id2),
                and_(Friendship.user_id1 == user_id2, Friendship.user_id2 == user_id1),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_friends(self, user_id: int):
        stmt = (
            select(User)
            .join(
                Friendship,
                or_(
                    and_(Friendship.user_id1 == user_id, User.user_id == Friendship.user_id2),
                    and_(Friendship.user_id2 == user_id, User.user_id == Friendship.user_id1),
                ),
            )
            .where(Friendship.is_active == True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_friend(self, user_id: int, friend_id: int):
        friendship = Friendship(user_id1=min(user_id, friend_id), user_id2=max(user_id, friend_id))
        self.session.add(friendship)
        await self.session.commit()
        return True
