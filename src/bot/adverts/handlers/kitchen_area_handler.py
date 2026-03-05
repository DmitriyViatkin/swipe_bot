from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.keyboard.yes_or_no_keyboards import yes_no_kb
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(
    AdvertsState.waiting_for_kitchen_area,
    ~F.text.in_([__("btn_cancel_a"), __("btn_back_a")]),
)
async def area_kitchen_handler(message: types.Message, state: FSMContext):

    await state.update_data(kitchen_area=message.text)

    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    try:
        # Заменяем запятую на точку для корректного преобразования
        area_val = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer(_("error_invalid_float"))
        return

    await state.update_data(kitchen_area=area_val)

    await state.set_state(AdvertsState.waiting_for_is_balcony)
    await message.answer(_("is_there_balcony"), reply_markup=yes_no_kb())
