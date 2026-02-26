from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import (
    get_control_keyboard,
    get_photo_keyboard,
)

router = Router()


@router.message(F.text == __("btn_back"))
async def process_back_navigation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegistrationState.waiting_for_last_name:
        await state.set_state(RegistrationState.waiting_for_first_name)
        await message.answer(_("enter_first_name"), reply_markup=get_control_keyboard())

    elif current_state == RegistrationState.waiting_for_phone:
        await state.set_state(RegistrationState.waiting_for_last_name)
        await message.answer(_("enter_last_name"), reply_markup=get_control_keyboard())

    elif current_state == RegistrationState.waiting_for_email:
        await state.set_state(RegistrationState.waiting_for_phone)
        await message.answer(_("enter_phone"), reply_markup=get_control_keyboard())

    elif current_state == RegistrationState.waiting_for_photo:
        await state.set_state(RegistrationState.waiting_for_email)
        await message.answer(_("enter_email"), reply_markup=get_control_keyboard())

    elif current_state == RegistrationState.waiting_for_password:
        await state.set_state(RegistrationState.waiting_for_photo)
        await message.answer(
            _("enter_photo_or_skip"), reply_markup=get_photo_keyboard()
        )

    elif current_state == RegistrationState.confirm_data:
        # Якщо юзер хоче повернутися з фінального екрану — кидаємо на пароль
        await state.set_state(RegistrationState.waiting_for_password)
        await message.answer(_("enter_password"), reply_markup=get_control_keyboard())
