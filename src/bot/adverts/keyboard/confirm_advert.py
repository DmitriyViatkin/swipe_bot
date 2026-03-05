from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def get_confirm_advert_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=_("btn_confirm_and_publish"))
    builder.button(text=_("btn_cancel_a"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
