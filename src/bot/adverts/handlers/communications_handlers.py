from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.keyboard.control_panel import control_keyboard
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(
    AdvertsState.waiting_for_communication,
    ~F.text.in_([__("btn_cancel_a"), __("btn_back_a")]),
)
async def communication_handler(message: types.Message, state: FSMContext):
    await state.update_data(communication=message.text)

    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    await state.update_data(communication=message.text)
    await state.set_state(AdvertsState.waiting_for_rooms)
    await message.answer(_("enter_rooms"), reply_markup=control_keyboard())
