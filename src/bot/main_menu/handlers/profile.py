from aiogram import Router, types, F
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.fsm.context import FSMContext
from src.api_client.base_api import BaseAPIClient
from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)

router = Router()


@router.message(F.text == __("btn_my_profile"))
async def profile_handler(
    message: types.Message, state: FSMContext, api: BaseAPIClient
):

    user_data = await state.get_data()
    token = user_data.get("access_token")
    user_id = user_data.get("user_id")

    if not token or not user_id:
        await message.answer(
            "_no_authorization.", reply_markup=get_auth_choice_keyboard()
        )
        return
    user_profile = await api.get_user_data(user_id, token)

    if "error" in user_profile:
        await message.answer(f"Помилка завантаження: {user_profile['error']}")
        return
    response_text = (
        f"👤 **__you_profile**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**_name:** {user_profile.get('first_name')} {user_profile.get('last_name')}\n"
        f"**_email:** `{user_profile.get('email')}`\n"
        f"**_phone:** {user_profile.get('phone') or '_no'}\n"
    )

    await message.answer(response_text, parse_mode="Markdown")
