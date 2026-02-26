from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.authorization.states import RegistrationState

router = Router()


@router.callback_query(RegistrationState.confirm_data, F.data == "finish_registration")
async def process_finish_registration(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.edit_text(text=_("registration_finished_success"))
    # Можна надіслати головне меню бота
    # await callback.message.answer(_("welcome_message"), reply_markup=main_menu())
    await callback.answer()
