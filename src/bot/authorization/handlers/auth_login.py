from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from src.bot.authorization.states import AuthStates
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard

router = Router()


@router.message(F.text == __("btn_login"))
async def start_login(message: types.Message, state: FSMContext):

    await state.set_state(AuthStates.waiting_for_email)

    await message.answer(_("enter_email"), reply_markup=get_control_keyboard())


# --- 1. Обробка кнопки "Скасувати" ---
@router.message(F.text == __("btn_cancel"))
async def cancel_auth(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        _("auth_choice_text"), reply_markup=types.ReplyKeyboardRemove()
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
