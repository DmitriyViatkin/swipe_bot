from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from src.bot.authorization.states import AuthStates
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard
from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)

router = Router()


BACK_TRANSITIONS = {
    AuthStates.waiting_for_password.state: (  # .state даёт строку "AuthStates:waiting_for_password"
        AuthStates.waiting_for_email,
        "enter_email",
        lambda: get_control_keyboard(show_back=False),
    ),
    AuthStates.waiting_for_email.state: (
        None,
        "auth_choice_text",
        get_auth_choice_keyboard,
    ),
}


@router.message(F.text == __("btn_back_b"))
async def go_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()  # строка "AuthStates:waiting_for_email"
    transition = BACK_TRANSITIONS.get(current_state)  # теперь находит правильно

    if transition is None:
        print("auth_choice_text")
        await message.answer(
            _("auth_choice_text"), reply_markup=get_auth_choice_keyboard()
        )
        return

    prev_state, text_key, get_keyboard = transition

    if prev_state is None:
        await state.clear()
    else:
        await state.set_state(prev_state)

    await message.answer(_(text_key), reply_markup=get_keyboard())


@router.message(F.text == __("btn_cancel_b"))
async def cancel_auth(message: types.Message, state: FSMContext):
    print("btn_cancel_b")
    await state.clear()
    await message.answer(_("auth_choice_text"), reply_markup=get_auth_choice_keyboard())
