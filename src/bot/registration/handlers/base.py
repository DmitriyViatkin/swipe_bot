from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from src.bot.registration.keyboards.keyboard import get_auth_choice_keyboard

router = Router()


@router.message(F.text == __("btn_cancel"))
async def cancel_registration(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()

    await message.answer(_("auth_cancelled"), reply_markup=types.ReplyKeyboardRemove())

    await message.answer(_("auth_choice_text"), reply_markup=get_auth_choice_keyboard())
