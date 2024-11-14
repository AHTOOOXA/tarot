from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.infrastructure.i18n import i18n


def command_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=i18n("ask_question"), callback_data="cmd_question")
    kb.button(text=i18n("daily_card"), callback_data="cmd_daily")
    kb.button(text=i18n("start_reading"), callback_data="cmd_reading")
    kb.adjust(1, 1, 1)
    return kb.as_markup()
