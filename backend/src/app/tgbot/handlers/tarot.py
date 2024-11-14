from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from app.infrastructure.i18n import i18n
from app.schemas.tarot import DailyReadingMessage
from app.schemas.users import UserSchema
from app.services.requests import RequestsService

router = Router()


class TarotStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_spread_type = State()


async def _send_daily_card(message: types.Message, user: UserSchema, services: RequestsService):
    await message.answer(i18n("processing_daily_card"))
    card = await services.tarot.get_random_card()
    await message.answer_photo(
        photo=card.image_url,
        caption=card.name,
    )  # TODO: localize
    reading: DailyReadingMessage = await services.tarot.get_daily_reading(user=user, card=card)
    await message.answer(reading.interpretation)


async def _handle_question(message: types.Message, state: FSMContext):
    await state.set_state(TarotStates.waiting_for_question)
    await message.answer(i18n("ask_question_prompt"))


@router.message(TarotStates.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext, user: UserSchema, services: RequestsService):
    reading = await services.tarot.get_question_reading(user=user, question=message.text)
    await state.clear()
    await message.answer(reading)


@router.callback_query(lambda c: c.data == "cmd_daily")
async def daily_card_callback(callback: CallbackQuery, user: UserSchema, services: RequestsService):
    await callback.answer()
    await _send_daily_card(callback.message, user, services)


@router.callback_query(lambda c: c.data == "cmd_question")
async def question_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _handle_question(callback.message, state)
