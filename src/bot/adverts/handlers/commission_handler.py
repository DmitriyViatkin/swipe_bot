from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from ..handlers.show_summary import process_show_summary
from ..keyboard.control_panel import control_keyboard

router = Router()


@router.message(
    AdvertsState.waiting_for_commission,
    ~F.text.in_([__("btn_cancel_a"), __("btn_back_a")]),
)
async def commission_handler(message: types.Message, state: FSMContext):
    await state.update_data(commission=message.text)

    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    await state.update_data(commission=message.text)
    await state.set_state(AdvertsState.waiting_for_description)
    await message.answer(_("enter_description"), reply_markup=control_keyboard())
