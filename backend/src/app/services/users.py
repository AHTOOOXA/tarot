import logging

from app.exceptions import FriendAlreadyExistsException, UserNotFoundException
from app.schemas.users import UserSchema
from app.services.base import BaseService

logger = logging.getLogger(__name__)


class UserService(BaseService):
    async def get_or_create_user(self, user_id: int, first_name: str, username: str):
        user = await self.repo.users.get_or_create_user(user_id, first_name, username)

        if user.created_at == user.updated_at:
            logger.info(f"User {user_id} created")
            # TODO: Some initial logic here
            # TODO: posthog analytics record here

        return UserSchema.model_validate(user)

    async def get_user_by_id(self, user_id: int):
        return await self.repo.users.get_user_by_id(user_id)

    async def get_profile(self, user_id: int):
        user = await self.repo.users.get_user_by_id(user_id)
        return {
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code,
            "photo_url": user.photo_url,
        }

    async def get_friends(self, user_id: int):
        return await self.repo.users.get_friends(user_id)

    async def add_friend(self, user_id: int, friend_id: int):
        friend = await self.repo.users.get_user_by_id(friend_id)
        if friend is None:
            raise UserNotFoundException(f"User with id {friend_id} not found")
        if await self.is_friend(user_id, friend_id):
            raise FriendAlreadyExistsException(f"User {friend_id} is already a friend of {user_id}")
        await self.repo.users.add_friend(user_id, friend.user_id)

    async def update_user(self, user_id: int, user_data: dict):
        # TODO: add validation and security checks
        await self.repo.users.update_user(user_id, user_data)

    async def is_friend(self, user_id1: int, user_id2: int) -> bool:
        friendship = await self.repo.users.get_friendship(user_id1, user_id2)
        return friendship is not None and friendship.is_active
