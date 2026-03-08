from aiogram import Router, types, F
from aiogram.utils.i18n import lazy_gettext as __
from src.bot.main_menu.keyboards.keyboard_menu import main_menu

router = Router()


@router.message(F.text == __("btn_my_menu"))
async def main_handler(message: types.Message):
    text = f"🏠 *{__('main_menu_title')}*\n"
    await message.answer(text=text, reply_markup=main_menu(), parse_mode="Markdown")
