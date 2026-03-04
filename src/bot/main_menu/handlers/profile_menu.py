from aiogram import Router, types, F
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from src.bot.main_menu.keyboards.profile_keyboard import profile_menu


router = Router()


@router.message(F.text == __("btn_profile_data"))
async def personal_menu(
    message: types.Message,
):

    await message.answer(_("Your_menu"), reply_markup=profile_menu())
