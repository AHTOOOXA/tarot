from app.services.base import BaseService


class UserService(BaseService):
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
        await self.repo.users.add_friend(user_id, friend.user_id)

    async def update_user(self, user_id: int, user_data: dict):
        # TODO: add validation and security checks
        await self.repo.users.update_user(user_id, user_data)
