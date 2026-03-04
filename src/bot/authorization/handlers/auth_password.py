from aiogram.fsm.context import FSMContext
from src.api_client.base_api import BaseAPIClient
from src.bot.authorization.states import AuthStates
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from src.bot.main_menu.keyboards.keyboard_menu import main_menu

router = Router()


@router.message(AuthStates.waiting_for_password)
async def process_password(
    message: types.Message, state: FSMContext, api: BaseAPIClient
):
    password = message.text.strip()
    user_data = await state.get_data()
    email = user_data.get("email")

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    msg_status = await message.answer("🔄 Перевірка даних на сервері...")

    telegram_id = message.from_user.id

    login_resp = await api.login(email, password, telegram_id)

    if "error" in login_resp:
        await msg_status.edit_text(
            f"❌ Помилка: {login_resp['error']}\n\nСпробуйте ввести Email ще раз:"
        )
        await state.set_state(AuthStates.waiting_for_email)
        return

    token = api.user_tokens.get(telegram_id)
    if not token:
        await msg_status.edit_text(
            "❌ Помилка: Не вдалося отримати токен після логіна."
        )
        return

    user_id = api._decode_user_id(token)
    if not user_id:
        await msg_status.edit_text(
            "❌ Помилка: Не вдалося отримати ID користувача з токена."
        )
        return

    await state.update_data(user_id=user_id, auth_status=True)

    await msg_status.delete()
    await message.answer(
        f"✅ Авторизація успішна!\n\nВи увійшли як: **{email}**\nВаш ID: `{user_id}`",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

    await state.set_state(None)
