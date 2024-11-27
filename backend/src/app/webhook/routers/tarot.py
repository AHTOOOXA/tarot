import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.infrastructure.i18n import i18n
from app.schemas.tarot import TarotCard
from app.schemas.users import UserSchema
from app.services.requests import RequestsService
from app.tgbot.services import broadcaster
from app.webhook.auth import get_twa_user
from app.webhook.dependencies.service import get_services

router = APIRouter(prefix="/tarot")

logger = logging.getLogger(__name__)


@router.get("/draw_daily_card")
async def draw_daily_card(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> List[TarotCard]:
    return await services.tarot.get_random_cards(5)


@router.post("/select_daily_card")
async def select_daily_card(
    card: TarotCard,
    request: Request,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
):
    reading = await services.tarot.get_daily_reading(user, card)
    # TODO: fix it doesn't work, do it with a rabbit queue
    logger.info(f"Sending message to {user.user_id}")
    # await broadcaster.send_message(
    #     user.user_id,
    #     i18n("daily_card_result").format(card_name=reading.card.name, interpretation=reading.interpretation),
    # )
    return reading
