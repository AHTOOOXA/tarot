from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import tgbot_config

domain = tgbot_config.web_app_domain


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="BRO APP!", web_app=WebAppInfo(url=domain))
    kb.button(
        text="BRO CHANNEL!",
        web_app=WebAppInfo(url=f"{domain}/see_a_doctor"),
    )
    kb.adjust(1, 1)
    return kb.as_markup()
