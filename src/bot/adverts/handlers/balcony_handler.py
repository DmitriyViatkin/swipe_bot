from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(
    AdvertsState.waiting_for_is_balcony,
    ~F.text.in_([__("btn_cancel_r"), __("btn_back")]),
)
async def balcony_handler(message: types.Message, state: FSMContext):
    await state.update_data(is_balcony=message.text)

    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    is_balcony = True if message.text == _("yes") else False

    await state.update_data(is_balcony=is_balcony)
    await state.set_state(AdvertsState.waiting_for_commission)
    await message.answer(_("enter_commission"))
