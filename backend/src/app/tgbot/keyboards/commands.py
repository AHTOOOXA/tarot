from aiogram.utils.keyboard import InlineKeyboardBuilder


def command_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Ask a Question 🔮", callback_data="cmd_question")
    kb.button(text="Daily Card 🔮", callback_data="cmd_daily")
    kb.button(text="Start Some Reading 🔮", callback_data="cmd_reading")
    kb.adjust(1, 1, 1)
    return kb.as_markup()
