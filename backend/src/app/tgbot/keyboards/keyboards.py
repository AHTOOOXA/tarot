from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.config import tgbot_config
from app.infrastructure.i18n import i18n


# TODO: later finish this menu keyboard
def menu_keyboard():
    kb = ReplyKeyboardBuilder()
    # kb.button(text=i18n("open_app"), web_app=WebAppInfo(url=f"{tgbot_config.web_app_domain}"))
    kb.button(text=i18n("open_menu"))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def settings_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text=i18n("language_button").format(lang=i18n("languages.current_language")),
        callback_data="cmd_settings_change_language",
    )
    kb.button(text=i18n("back_to_menu"), callback_data="cmd_back_to_menu")
    kb.adjust(1, 1)
    return kb.as_markup()


def settings_change_language_keyboard():
    languages = i18n("languages")
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"settings_set_lang_{code}")]
        for code, name in languages.items()
        if code != "current_language"
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def command_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n("daily_card"), callback_data="cmd_daily")
    kb.button(text=i18n("ask_question"), callback_data="cmd_question")
    # kb.button(text=i18n("start_reading"), callback_data="cmd_reading")
    kb.button(text=i18n("pay"), callback_data="cmd_pay")
    kb.button(text=i18n("settings"), callback_data="cmd_settings")
    kb.adjust(1, 1, 1, 1)
    return kb.as_markup()


def terms_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(
        text=i18n("language_button").format(lang=i18n("languages.current_language")),
        callback_data="cmd_change_language",
    )
    kb.button(text=i18n("accept_terms"), callback_data="accept_terms")
    kb.adjust(1)
    return kb.as_markup()


def language_selection_keyboard() -> InlineKeyboardMarkup:
    languages = i18n("languages")
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"set_lang_{code}")]
        for code, name in languages.items()
        if code != "current_language"
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def pay_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n("buy_10_questions"), callback_data="pay_10_questions")
    kb.button(text=i18n("buy_week"), callback_data="pay_week")
    kb.button(text=i18n("buy_month"), callback_data="pay_month")
    kb.button(text=i18n("back_to_menu"), callback_data="cmd_back_to_menu")
    kb.adjust(1)
    return kb.as_markup()


def draw_card_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n("draw_card_button"), web_app=WebAppInfo(url=f"{tgbot_config.web_app_domain}/draw"))
    kb.adjust(1)
    return kb.as_markup()
