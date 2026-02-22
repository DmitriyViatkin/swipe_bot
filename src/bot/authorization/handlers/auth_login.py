from aiogram.fsm.context import FSMContext

from src.bot.authorization.states import AuthStates
from aiogram import Router, F, types

router = Router()


@router.callback_query(F.data == "auth_login")
async def start_login(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text("📧 Введіть ваш Email:")

    # Вмикаємо стан "очікування емейла"
    await state.set_state(AuthStates.waiting_for_email)
    await callback.answer()
