from aiogram import Router, types, F
from src.bot.authorization.states import RegistrationState
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(RegistrationState.confirm_data, F.data.startswith("edit_"))
async def handle_edit_field(callback: types.CallbackQuery, state: FSMContext):
    field = callback.data.replace("edit_", "")

    states_map = {
        "first_name": RegistrationState.waiting_for_first_name,
        "last_name": RegistrationState.waiting_for_last_name,
        "phone": RegistrationState.waiting_for_phone,
        "email": RegistrationState.waiting_for_email,
        "photo": RegistrationState.waiting_for_photo,
        "password": RegistrationState.waiting_for_password,
    }

    await state.set_state(states_map[field])

    await callback.message.delete()

    await callback.message.answer(_(f"enter_new_{field}"))
    await callback.answer()
