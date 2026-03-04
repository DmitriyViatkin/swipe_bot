from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.bot.main_menu.keyboards.keyboard_menu import main_menu
from aiogram.utils.i18n import lazy_gettext as __

router = Router()


@router.message(F.text == __("btn_cancel_a"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Створення оголошення скасовано.", reply_markup=main_menu())
