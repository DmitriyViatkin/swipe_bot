from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.authorization.states import RegistrationState
from src.api_client.base_api import BaseAPIClient
from src.bot.main_menu.keyboards.keyboard_menu import main_menu

router = Router()


@router.callback_query(RegistrationState.confirm_data, F.data == "finish_registration")
async def process_finish_registration(
    callback: types.CallbackQuery, state: FSMContext, api: BaseAPIClient
):
    user_data = await state.get_data()

    payload = {
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "phone": user_data.get("phone"),
        "email": user_data.get("email"),
        "photo": user_data.get("photo") or "",
        "password": user_data.get("password"),
        "role": "client",
    }

    result = await api.registration(**payload)

    if "error" in result:
        await callback.message.answer(
            f"❌ {_('registration_failed')}\n{result['error']}"
        )
    else:
        await state.clear()

        await callback.message.edit_text(_("registration_complete_success"))

        await callback.message.answer(_("welcome_msg"), reply_markup=main_menu())

    await callback.answer()
