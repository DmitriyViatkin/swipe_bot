from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def profile_menu():

    builder = ReplyKeyboardBuilder()
    builder.button(text=_("btn_my_adverts"))
    builder.button(text=_("btn_my_profile"))
    builder.button(text=_("btn_create_advert"))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
