from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def get_control_keyboard(show_back: bool = True):
    builder = ReplyKeyboardBuilder()

    if show_back:
        builder.button(text=_("btn_back"))

    builder.button(text=_("btn_cancel"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
