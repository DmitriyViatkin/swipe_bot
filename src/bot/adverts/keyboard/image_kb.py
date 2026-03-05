from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _, lazy_gettext as __


def finish_images_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text=_("btn_skip"))
    builder.button(text=str(__("btn_finish_loading")))
    builder.button(text=str(__("btn_back_a")))
    builder.button(text=str(__("btn_cancel_a")))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
