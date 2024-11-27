import logging
from typing import List

from aiogram import Bot
from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.schemas.tarot import TarotCard
from app.schemas.users import UserSchema
from app.services.requests import RequestsService
from app.tgbot.services import broadcaster
from app.webhook.auth import get_twa_user
from app.webhook.dependencies.bot import get_bot
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
    bot: Bot = Depends(get_bot),
):
    reading = await services.tarot.get_daily_reading(user, card)
    await broadcaster.send_message(bot, user.user_id, reading.interpretation)
    return reading
