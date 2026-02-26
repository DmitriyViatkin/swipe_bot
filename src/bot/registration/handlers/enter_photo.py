from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.authorization.states import RegistrationState
from src.bot.registration.keyboards.keyboard import get_control_keyboard

router = Router()


@router.message(RegistrationState.waiting_for_photo)
async def enter_photo(message: types.Message, state: FSMContext):
    if message.photo:
        photo_id = message.photo[-1].file_id
        await state.update_data(photo=photo_id)
    else:
        await state.update_data(photo=None)

    await state.set_state(RegistrationState.waiting_for_password)
    await message.answer(_("enter_password"), reply_markup=get_control_keyboard())
