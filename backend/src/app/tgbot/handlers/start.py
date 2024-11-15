from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from app.infrastructure.database.models.users import User
from app.infrastructure.database.repo.requests import RequestsRepo
from app.infrastructure.files import file_manager
from app.infrastructure.i18n import i18n
from app.tgbot.keyboards.commands import command_keyboard, terms_keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, user: User, repo: RequestsRepo):
    welcome_image = FSInputFile(file_manager.get_image_path("welcome.jpeg"))

    await message.answer_photo(
        photo=welcome_image,
        caption=i18n("welcome_with_terms").format(terms_url="https://google.com"),
        reply_markup=terms_keyboard(),
    )


@router.callback_query(lambda c: c.data == "accept_terms")
async def accept_terms(callback: types.CallbackQuery, user: User, repo: RequestsRepo):
    await callback.answer()

    await callback.message.answer(
        i18n("welcome_after_terms"),
        reply_markup=command_keyboard(),
    )
