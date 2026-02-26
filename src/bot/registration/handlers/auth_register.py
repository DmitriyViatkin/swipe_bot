from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.authorization.states import RegistrationState
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard

router = Router()


@router.message(F.text == __("btn_register"))
async def start_registration(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationState.waiting_for_first_name)

    await message.answer(_("enter_first_name"), reply_markup=get_control_keyboard())


@router.message(F.text == __("btn_cancel"))
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        _("auth_choice_text"), reply_markup=types.ReplyKeyboardRemove()
    )
