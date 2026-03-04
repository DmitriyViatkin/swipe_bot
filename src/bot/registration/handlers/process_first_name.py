from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import get_control_keyboard

router = Router()


@router.message(
    RegistrationState.waiting_for_first_name,
    ~F.text.in_([__("btn_cancel_r"), __("btn_back")]),
)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)

    await state.set_state(RegistrationState.waiting_for_last_name)
    await message.answer(_("enter_last_name"), reply_markup=get_control_keyboard())
