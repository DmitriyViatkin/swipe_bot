from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def main_menu():

    builder = ReplyKeyboardBuilder()
    builder.button(text=_("btn_adverts"))
    builder.button(text=_("btn_profile_data"))
    builder.button(text=_("btn_create_advert"))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
