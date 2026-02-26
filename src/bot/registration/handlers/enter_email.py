from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import get_photo_keyboard
from src.bot.registration.keyboards.get_registration_confirm_keyboard import (
    get_registration_confirm_keyboard,
)

router = Router()


@router.message(RegistrationState.waiting_for_email)
async def enter_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
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
        await state.set_state(RegistrationState.waiting_for_photo)
        await message.answer(
            _("enter_photo_or_skip"), reply_markup=get_photo_keyboard()
        )
