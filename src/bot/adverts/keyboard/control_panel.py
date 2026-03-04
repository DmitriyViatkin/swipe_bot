from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import lazy_gettext as __


def control_keyboard(show_back: bool = True):
    builder = ReplyKeyboardBuilder()

    if show_back:
        builder.button(text=str(__("btn_back_a")))

    builder.button(text=str(__("btn_cancel_a")))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
