from aiogram import Router, types
from aiogram.filters import CommandStart

from app.infrastructure.database.models.users import User
from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.i18n import i18n
from app.tgbot.keyboards.commands import command_keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, user: User, repo: RequestsRepo):
    await message.answer(
        i18n("welcome"),
        reply_markup=command_keyboard(),
    )
