from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def get_registration_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=_("edit_first_name"), callback_data="edit_first_name")
    builder.button(text=_("edit_last_name"), callback_data="edit_last_name")
    builder.button(text=_("edit_phone_name"), callback_data="edit_phone")
    builder.button(text=_("edit_email_name"), callback_data="edit_email")
    builder.button(text=_("edit_photo_name"), callback_data="edit_photo")
    builder.button(text=_("edit_password_"), callback_data="edit_password")
    builder.button(
        text=_("finish_registration_btn"), callback_data="finish_registration"
    )
    builder.adjust(1)

    return builder.as_markup()
