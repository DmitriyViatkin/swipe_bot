from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import (
    get_auth_choice_keyboard,
    get_language_keyboard,
    get_control_keyboard,
)


from aiogram.utils.i18n import lazy_gettext as __

router = Router()


@router.message(F.text == __("btn_cancel_r"))
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(_("auth_choice_text"), reply_markup=get_language_keyboard())


@router.message(F.text == __("btn_back"))
async def go_back_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state in (None, RegistrationState.waiting_for_first_name):
        await state.clear()
        await message.answer(
            _("auth_choice_text"), reply_markup=get_auth_choice_keyboard()
        )

    state_map = {
        RegistrationState.waiting_for_last_name: (
            RegistrationState.waiting_for_first_name,
            _("enter_first_name"),
        ),
        RegistrationState.waiting_for_phone: (
            RegistrationState.waiting_for_last_name,
            _("enter_last_name"),
        ),
        RegistrationState.waiting_for_email: (
            RegistrationState.waiting_for_phone,
            _("enter_phone"),
        ),
        RegistrationState.waiting_for_photo: (
            RegistrationState.waiting_for_email,
            _("enter_email"),
        ),
        RegistrationState.waiting_for_password: (
            RegistrationState.waiting_for_photo,
            _("enter_photo"),
        ),
        RegistrationState.confirm_data: (
            RegistrationState.waiting_for_password,
            _("enter_password"),
        ),
    }

    if current_state in state_map:
        new_state, text = state_map[current_state]
        await state.set_state(new_state)
        await message.answer(text, reply_markup=get_control_keyboard())

    if current_state in state_map:
        new_state, text = state_map[current_state]
        await state.set_state(new_state)
        await message.answer(text, reply_markup=get_control_keyboard())
