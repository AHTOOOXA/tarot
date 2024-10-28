import base64

from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.rabbit.producer import RabbitMQProducer
from app.schemas.invites import InviteTokens
from app.services.base import BaseService


class InvitesService(BaseService):
    def __init__(
        self,
        repo: RequestsRepo,
        producer: RabbitMQProducer,
    ):
        super().__init__(repo, producer)
        # Simple offset key (could be loaded from env vars)
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
        group_token = await self.generate_token(str(user_id))
        return InviteTokens(user_token=user_token, group_token=group_token)

    async def create_invite(self, user_id: int) -> InviteTokens:
        tokens = await self.get_invite_tokens(user_id)
        # TODO: Save the invite to the database with user_id and tokens
        return tokens

    async def validate_invite(self, invite_tokens: InviteTokens) -> bool:
        user_id = await self.decrypt_token(invite_tokens.user_token)
        group_id = await self.decrypt_token(invite_tokens.group_token)
        print("decrypted", user_id, group_id)
        # TODO: Validate the invite in the database
        return True
