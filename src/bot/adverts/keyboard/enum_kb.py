from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from enum import Enum
from aiogram.utils.i18n import gettext as _, lazy_gettext as __


def get_enum_kb(enum_class: type[Enum]):
    builder = ReplyKeyboardBuilder()
    for item in enum_class:
        builder.button(text=_(item.value))

    builder.adjust(2)
    builder.row(
        types.KeyboardButton(text=str(__("btn_back_a"))),
        types.KeyboardButton(text=str(__("btn_cancel_a"))),
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
