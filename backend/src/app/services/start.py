import base64

from app.schemas.start import StartData, StartParams
from app.services.base import BaseService


class StartService(BaseService):
    async def process_start(self, start_params: StartParams) -> StartData:
        return StartData(current_user=None, inviter=None)
