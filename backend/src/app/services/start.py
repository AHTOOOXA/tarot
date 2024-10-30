from app.schemas.start import StartData, StartParams
from app.schemas.users import UserSchema
from app.services.base import BaseService


class StartService(BaseService):
    async def process_start(self, user: UserSchema, start_params: StartParams) -> StartData:
        current_user = user

        inviter = None
        if start_params.user_token and start_params.group_token:
            inviter = await self.services.invites.process_invite(
                start_params.user_token, start_params.group_token, current_user.user_id
            )

        return StartData(
            current_user=current_user,
            inviter=inviter,
        )
