from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.adverts.adverts_state import AdvertsState
from src.api_client.base_api import BaseAPIClient
from src.bot.main_menu.keyboards.keyboard_menu import main_menu
from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)

router = Router()


@router.callback_query(AdvertsState.confirm_data, F.data == "finish_advert_publish")
async def process_finish_create_advert(
    callback: types.CallbackQuery, state: FSMContext, api: BaseAPIClient
):
    telegram_id = callback.from_user.id
    token = api.user_tokens.get(telegram_id)

    if not token:
        await callback.message.answer(
            "❌ Ошибка авторизации. Войдите заново.",
            reply_markup=get_auth_choice_keyboard(),
        )
        return

    user_data = await state.get_data()

    payload = {
        "build_id": 1,
        "address": user_data.get("address"),
        "appointment": user_data.get("appointment"),
        "layout": user_data.get("layout"),
        "state": user_data.get("state"),
        "heating": user_data.get("heating"),
        "payment": user_data.get("payment"),
        "communication": user_data.get("communication"),
        "rooms": int(user_data.get("rooms", 0)),
        "area": float(str(user_data.get("area", 0)).replace(",", ".")),
        "kitchen_area": float(str(user_data.get("kitchen_area", 0)).replace(",", ".")),
        "is_balcony": bool(user_data.get("is_balcony")),
        "commission": float(str(user_data.get("commission", 0)).replace(",", ".")),
        "description": user_data.get("description"),
        "price": float(str(user_data.get("price", 0)).replace(",", ".")),
        "images": user_data.get("images", []),
    }
    print(payload)
    result = await api.create_adverts(token=token, **payload)

    if "error" in result:
        await callback.message.answer(
            f"❌ {_('advert_creation_failed')}\n{result['error']}"
        )
        return

    await state.clear()

    await callback.message.edit_text(_("advert_created_success_msg"))
    await callback.message.answer(_("main_menu_label"), reply_markup=main_menu())

    await callback.answer()
