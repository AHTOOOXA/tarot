from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from app.config import tgbot_config
from app.infrastructure.files import file_manager
from app.infrastructure.i18n import i18n
from app.schemas.users import UpdateUserRequest, UserSchema
from app.services.requests import RequestsService
from app.tgbot.keyboards.commands import (
    command_keyboard,
    language_selection_keyboard,
    pay_keyboard,
    terms_keyboard,
)

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, user: UserSchema, services: RequestsService):
    welcome_image = FSInputFile(file_manager.get_image_path("welcome.jpeg"))
    terms_url = f"{tgbot_config.api_domain}/static/oferta-tarot.pdf"

    if not user.is_terms_accepted:
        await message.answer_photo(
            photo=welcome_image,
            caption=i18n("welcome_with_terms").format(terms_url=terms_url),
            reply_markup=terms_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            i18n("welcome_after_terms"),
            reply_markup=command_keyboard(),
        )


@router.callback_query(lambda c: c.data == "accept_terms")
async def accept_terms(callback: types.CallbackQuery, user: UserSchema, services: RequestsService):
    await callback.answer()
    await services.users.update_user(user.user_id, UpdateUserRequest(is_terms_accepted=True))
    await callback.message.answer(
        i18n("welcome_after_terms"),
        reply_markup=command_keyboard(),
    )


@router.callback_query(lambda c: c.data == "change_language")
async def change_language(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=language_selection_keyboard())


@router.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery, user: UserSchema, services: RequestsService):
    lang_code = callback.data.split("_")[2]

    updated_user = await services.users.update_user(user.user_id, UpdateUserRequest(app_language_code=lang_code))
    i18n.update_locale(updated_user.app_language_code)

    await callback.message.edit_caption(
        caption=i18n("welcome_with_terms").format(terms_url="https://google.com"),
    )
    await callback.message.edit_reply_markup(reply_markup=terms_keyboard(lang_code))


@router.callback_query(lambda c: c.data == "cmd_pay")
async def pay_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=pay_keyboard())


@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=i18n("welcome_after_terms"), reply_markup=command_keyboard())
