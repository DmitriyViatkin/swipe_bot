from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import get_control_keyboard
from src.bot.registration.keyboards.get_registration_confirm_keyboard import (
    get_registration_confirm_keyboard,
)

router = Router()


@router.message(RegistrationState.waiting_for_phone)
async def enter_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()

    if "password" in data:
        await state.set_state(RegistrationState.confirm_data)
        await message.answer(
            _("data_updated"), reply_markup=types.ReplyKeyboardRemove()
        )
        await message.answer(
            _("data_updated"), reply_markup=get_registration_confirm_keyboard()
        )
    else:
        await state.set_state(RegistrationState.waiting_for_email)
        await message.answer(_("enter_email"), reply_markup=get_control_keyboard())
