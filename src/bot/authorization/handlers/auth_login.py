from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from src.bot.authorization.states import AuthStates
from src.bot.authorization.keyboards.control_keyboards import get_control_keyboard

router = Router()


@router.message(
    F.text == __("btn_login"), ~F.text.in_([__("btn_cancel_b"), __("btn_back_b")])
)
async def start_login(message: types.Message, state: FSMContext):

    await state.set_state(AuthStates.waiting_for_email)

    await message.answer(_("enter_email"), reply_markup=get_control_keyboard())
