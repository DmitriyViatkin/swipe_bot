from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(
    AdvertsState.waiting_for_area, ~F.text.in_([__("btn_cancel_a"), __("btn_back_a")])
)
async def area_handler(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)

    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    try:
        area_val = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer(_("error_invalid_float"))
        return

    await state.update_data(area=area_val)
    await state.set_state(AdvertsState.waiting_for_kitchen_area)
    await message.answer(
        _("enter_area_kitchen"),
    )
