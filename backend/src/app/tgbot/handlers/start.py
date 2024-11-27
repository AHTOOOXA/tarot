from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from app.config import tgbot_config
from app.infrastructure.files import file_manager
from app.infrastructure.i18n import i18n
from app.schemas.users import UpdateUserRequest, UserSchema
from app.services.requests import RequestsService
from app.tgbot.keyboards.keyboards import (
    command_keyboard,
    language_selection_keyboard,
    menu_keyboard,
    pay_keyboard,
    settings_change_language_keyboard,
    settings_keyboard,
    terms_keyboard,
)

router = Router()


async def send_menu(message: types.Message | types.CallbackQuery):
    text = i18n("menu")
    if isinstance(message, types.CallbackQuery):
        await message.message.answer(text=text, reply_markup=command_keyboard())
    else:
        await message.answer(text=text, reply_markup=command_keyboard())


@router.message(CommandStart())
async def start_command(message: types.Message, user: UserSchema, services: RequestsService):
    if not user.is_terms_accepted:
        welcome_image = FSInputFile(file_manager.get_image_path("welcome.jpeg"))
        terms_url = f"{tgbot_config.api_domain}/static/oferta-tarot.pdf"
        await message.answer_photo(
            photo=welcome_image,
            caption=i18n("welcome_with_terms").format(terms_url=terms_url),
            reply_markup=terms_keyboard(),
            parse_mode="HTML",
        )
    else:
        await send_menu(message)


@router.callback_query(lambda c: c.data == "cmd_menu")
async def menu_command(callback: types.CallbackQuery):
    await callback.answer()
    await send_menu(callback)


@router.callback_query(lambda c: c.data == "cmd_back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=i18n("menu"))
    await callback.message.edit_reply_markup(reply_markup=command_keyboard())


@router.callback_query(lambda c: c.data == "cmd_settings")
async def settings_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=i18n("settings"))
    await callback.message.edit_reply_markup(reply_markup=settings_keyboard())


@router.callback_query(lambda c: c.data == "cmd_settings_change_language")
async def settings_change_language(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=settings_change_language_keyboard())


@router.callback_query(lambda c: c.data.startswith("settings_set_lang_"))
async def settings_set_language(callback: types.CallbackQuery, user: UserSchema, services: RequestsService):
    lang_code = callback.data.split("_")[-1]

    updated_user = await services.users.update_user(user.user_id, UpdateUserRequest(app_language_code=lang_code))
    i18n.update_locale(updated_user.app_language_code)

    await callback.message.edit_reply_markup(reply_markup=settings_keyboard())


@router.callback_query(lambda c: c.data == "accept_terms")
async def accept_terms(callback: types.CallbackQuery, user: UserSchema, services: RequestsService):
    await callback.answer()
    await services.users.update_user(user.user_id, UpdateUserRequest(is_terms_accepted=True))
    # TODO: later finish this menu keyboard
    # await callback.message.answer(text=i18n("welcome_after_terms"), reply_markup=menu_keyboard())
    await send_menu(callback)


@router.callback_query(lambda c: c.data == "cmd_change_language")
async def change_language(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=language_selection_keyboard())


@router.callback_query(lambda c: c.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery, user: UserSchema, services: RequestsService):
    lang_code = callback.data.split("_")[-1]

    updated_user = await services.users.update_user(user.user_id, UpdateUserRequest(app_language_code=lang_code))
    i18n.update_locale(updated_user.app_language_code)

    terms_url = f"{tgbot_config.api_domain}/static/oferta-tarot.pdf"

    await callback.message.edit_caption(
        caption=i18n("welcome_with_terms").format(terms_url=terms_url),
    )
    await callback.message.edit_reply_markup(reply_markup=terms_keyboard())


@router.callback_query(lambda c: c.data == "cmd_pay")
async def pay_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=pay_keyboard())


@router.callback_query(lambda c: c.data == "cmd_back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await send_menu(callback)
