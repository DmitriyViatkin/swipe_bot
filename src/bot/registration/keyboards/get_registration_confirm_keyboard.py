from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import lazy_gettext as __


def get_registration_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=str(__("edit_first_name")), callback_data="edit_first_name")
    builder.button(text=str(__("edit_last_name")), callback_data="edit_last_name")
    builder.button(text=str(__("edit_phone_name")), callback_data="edit_phone")
    builder.button(text=str(__("edit_email_name")), callback_data="edit_email")
    builder.button(text=str(__("edit_photo_name")), callback_data="edit_photo")
    builder.button(text=str(__("edit_password_")), callback_data="edit_password")
    builder.button(
        text=str(__("finish_registration_btn")), callback_data="finish_registration"
    )
    builder.adjust(1)

    return builder.as_markup()
