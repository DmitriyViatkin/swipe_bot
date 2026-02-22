from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(F.data.startswith("ua"))
def get_auth_choice_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=_("btn_login"), callback_data="auth_login")
    builder.button(text=_("btn_register"), callback_data="auth_register")

    builder.adjust(1)
    return builder.as_markup()
