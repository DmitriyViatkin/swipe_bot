from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import lazy_gettext as __


def get_auth_choice_keyboard():
    builder = ReplyKeyboardBuilder()

    # То же самое здесь
    builder.add(KeyboardButton(text=str(__("btn_login"))))
    builder.add(KeyboardButton(text=str(__("btn_register"))))
    builder.add(KeyboardButton(text=str(__("btn_back_to_lang"))))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
