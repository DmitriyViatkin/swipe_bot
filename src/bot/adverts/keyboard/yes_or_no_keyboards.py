from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram.utils.i18n import gettext as _


def yes_no_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text=_("yes"))
    builder.button(text=_("no"))
    builder.row(
        types.KeyboardButton(text=_("btn_back_a")),
        types.KeyboardButton(text=_("btn_cancel_a")),
    )
    return builder.as_markup(resize_keyboard=True)
