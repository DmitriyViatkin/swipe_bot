from aiogram.fsm.context import FSMContext
from src.api_client.base_api import BaseAPIClient
from src.bot.authorization.states import AuthStates
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest


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
    login_resp = await api.login(email, password)
    if "error" in login_resp:
        await msg_status.edit_text(
            f"❌ Помилка: {login_resp['error']}\n\nСпробуйте ввести Email ще раз:"
        )
        # Повертаємо юзера на початок вводу емейла
        await state.set_state(AuthStates.waiting_for_email)
        return

        # Якщо успіх — токен уже зберігся в об'єкті api.token
    await msg_status.edit_text(
        f"✅ Авторизація успішна!\n\n"
        f"Ви увійшли як: **{email}**\n"
        f"Переглянути профіль: /profile",
        parse_mode="Markdown",
    )

    await state.clear()
