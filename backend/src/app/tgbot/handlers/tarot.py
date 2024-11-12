from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.schemas.tarot import SpreadType
from app.services.requests import RequestsService

router = Router()


class TarotStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_spread_type = State()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Welcome to the Tarot Bot! 🔮\n\n"
        "Commands:\n"
        "/daily - Get your daily card\n"
        "/reading - Start a new reading\n"
        "/question - Ask a specific question"
    )


@router.message(Command("daily"))
async def daily_card(message: types.Message, service: RequestsService = None):
    if not service:
        raise ValueError("Service not found in middleware data")

    reading = await service.tarot.create_reading(user_id=message.from_user.id, spread_type=SpreadType.SINGLE)
    card = reading.cards[0]

    await message.answer_photo(
        photo=card.image_url, caption=f"Your daily card is: {card.name}\n\n{reading.interpretation}"
    )


@router.message(Command("question"))
async def ask_question(message: types.Message, state: FSMContext):
    await state.set_state(TarotStates.waiting_for_question)
    await message.answer("What question would you like to ask the cards?")


@router.message(TarotStates.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext, service: RequestsService = None):
    if not service:
        raise ValueError("Service not found in middleware data")

    reading = await service.tarot.create_reading(
        user_id=message.from_user.id, spread_type=SpreadType.THREE_CARD, question=message.text
    )

    await state.clear()

    media = [types.InputMediaPhoto(media=card.image_url) for card in reading.cards]
    await message.answer_media_group(media=media)
    await message.answer(reading.interpretation)
