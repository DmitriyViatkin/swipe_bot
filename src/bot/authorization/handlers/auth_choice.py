from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.bot.authorization.states import AuthStates

from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard
from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)

router = Router()


@router.message(F.text == __("uk"))
async def auth_choice(message: types.Message):
    await message.answer(
        text=_("Вход или регистрация"), reply_markup=get_auth_choice_keyboard()
    )


@router.message(F.text == __("btn_back"))
async def go_back_auth(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AuthStates.waiting_for_password:
        await state.set_state(AuthStates.waiting_for_email)
        await message.answer(_("enter_email"), reply_markup=get_control_keyboard())

    elif current_state == AuthStates.waiting_for_email:
        await state.clear()

        await message.answer(
            _("auth_choice_text"), reply_markup=types.ReplyKeyboardRemove()
        )
