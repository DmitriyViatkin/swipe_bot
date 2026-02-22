from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_language_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Ukrainian", callback_data="lang_ua")],
        [InlineKeyboardButton(text="Russian", callback_data="lang_ru")],
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
