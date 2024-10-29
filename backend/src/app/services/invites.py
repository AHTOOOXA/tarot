import base64
from typing import TYPE_CHECKING

from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.schemas.invites import InviteTokens
from app.schemas.users import GroupSchema, UserSchema
from app.services.base import BaseService

if TYPE_CHECKING:
    from app.services.requests import RequestsService


class InvitesService(BaseService):
    def __init__(
        self,
        repo: RequestsRepo,
        producer: RabbitMQProducer,
        services: "RequestsService",
    ):
        super().__init__(repo, producer, services)
        self.offset = 7355

    async def generate_token(self, value: str) -> str:
        """Convert value to an obscured token."""
        # Add offset to make it harder to guess original value
        num = int(value) + self.offset
        # Convert to bytes and encode in base64
        encoded = base64.urlsafe_b64encode(str(num).encode()).decode()
        return encoded

    async def decrypt_token(self, token: str) -> str:
        """Convert token back to original value."""
        try:
            # Decode base64 back to string
            decoded = base64.urlsafe_b64decode(token.encode()).decode()
            # Remove offset to get original value
            original = int(decoded) - self.offset
            return str(original)
        except Exception:
            return ""

    async def get_invite_tokens(self, user_id: int) -> InviteTokens:
        user_token = await self.generate_token(str(user_id))
        group_token = await self.generate_token(str(1))
        return InviteTokens(user_token=user_token, group_token=group_token)

    async def create_invite(self, user_id: int) -> InviteTokens:
        tokens = await self.get_invite_tokens(user_id)
        # TODO: Save the invite to the database with user_id and tokens
        return tokens

    async def validate_invite(self, user_token: str, group_token: str) -> UserSchema | GroupSchema | None:
        user_id = await self.decrypt_token(user_token)
        group_id = await self.decrypt_token(group_token)
        # TODO: Validate the invite in the database
        return None

    async def process_invite(self, user_token: str, group_token: str, user_to_add: int) -> GroupSchema | None:
        """
        Process a group invitation and add the user to the group and as friend to all members.

        Args:
            user_token: Token of the inviting user
            group_token: Token of the group
            user_to_add: User ID of the person to add to group

        Returns:
            bool: True if invitation was processed successfully, False otherwise
        """
        try:
            inviting_user_id = int(await self.decrypt_token(user_token))
            group_id = int(await self.decrypt_token(group_token))

            # Validate if inviting user is member of the group
            is_member = await self.repo.groups.is_member(group_id, inviting_user_id)
            if not is_member:
                return None

            # Add user to the group
            await self.repo.groups.add_member(group_id, user_to_add)

            # Get all group members
            group_members = await self.repo.groups.get_group_members(group_id)

            # Add user as friend to all group members (and vice versa)
            for member in group_members:
                if member.user_id != user_to_add:  # Don't try to friend yourself
                    # Check if friendship already exists
                    existing_friendship = await self.repo.users.get_friendship(member.user_id, user_to_add)
                    if not existing_friendship:
                        await self.repo.users.add_friend(member.user_id, user_to_add)

            group = await self.repo.groups.get_group(group_id)
            return group

        except (ValueError, TypeError):
            return None
