from aiogram.fsm.context import FSMContext

from src.bot.authorization.states import AuthStates
from aiogram import Router, types

router = Router()


@router.message(AuthStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text.strip()

    if "@" not in email or "." not in email:
        await message.answer("❌ Це не схоже на коректний Email. Спробуйте ще раз:")
        return
    await state.update_data(email=email)
    await message.answer("🔑 Дякую! Тепер введіть ваш пароль:")
    await state.set_state(AuthStates.waiting_for_password)
