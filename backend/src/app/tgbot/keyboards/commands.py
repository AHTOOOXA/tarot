from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.infrastructure.i18n import i18n


def command_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n("ask_question"), callback_data="cmd_question")
    kb.button(text=i18n("daily_card"), callback_data="cmd_daily")
    kb.button(text=i18n("start_reading"), callback_data="cmd_reading")
    kb.adjust(1, 1, 1)
    return kb.as_markup()


def terms_keyboard(current_lang: str = "en"):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"🌐 {i18n('your_language')}: {current_lang}. {i18n('change')}", callback_data="change_language")
    kb.button(text=i18n("accept_terms"), callback_data="accept_terms")
    kb.adjust(1)
    return kb.as_markup()


def language_selection_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    languages = [
        ("English", "en"),
        ("Русский", "ru"),
    ]

    buttons = [[InlineKeyboardButton(text=name, callback_data=f"set_lang_{code}")] for name, code in languages]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
