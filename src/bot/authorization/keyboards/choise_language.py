from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import lazy_gettext as __


def get_language_keyboard():

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=str(__("btn_lang_uk"))))
    builder.add(KeyboardButton(text=str(__("btn_lang_en"))))
    builder.add(KeyboardButton(text=str(__("btn_lang_ru"))))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
