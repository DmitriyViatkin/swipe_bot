from src.bot.authorization.states import RegistrationState
from aiogram.utils.i18n import gettext as _
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from src.bot.registration.keyboards.get_registration_confirm_keyboard import (
    get_registration_confirm_keyboard,
)

router = Router()


@router.message(RegistrationState.waiting_for_password)
async def process_password_and_show_summary(message: types.Message, state: FSMContext):

    old_data = await state.get_data()
    is_editing = "password" in old_data

    await state.update_data(password=message.text)

    data = await state.get_data()

    await state.set_state(RegistrationState.confirm_data)

    summary_text = (
        f"📋 **{_('check_your_data')}**\n\n"
        f"👤 {_('first_name')}: {data.get('first_name')}\n"
        f"👤 {_('last_name')}: {data.get('last_name')}\n"
        f"📞 {_('phone')}: {data.get('phone')}\n"
        f"📧 {_('email')}: {data.get('email')}\n"
        f"🖼 {_('photo')}: {'✅' if data.get('photo') else '❌'}\n"
        f"🔑 {_('password')}: {data.get('password')}"
    )

    if is_editing:
        await message.answer(
            _("data_updated"), reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            _("processing_data"), reply_markup=types.ReplyKeyboardRemove()
        )

    await message.answer(
        text=summary_text,
        reply_markup=get_registration_confirm_keyboard(),
        parse_mode="Markdown",
    )
