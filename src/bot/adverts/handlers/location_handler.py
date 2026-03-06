from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from ..adverts_state import AdvertsState
from src.enums import AppointmentEnum
from ..keyboard.enum_kb import get_enum_kb
from aiogram.utils.i18n import gettext as _
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(AdvertsState.waiting_for_location, F.location)
async def location_handler(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    await state.update_data(latitude=lat, longitude=lon)
    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
        return
    else:
        await state.set_state(AdvertsState.waiting_for_appointment)
        await message.answer(
            _("select_appointment"), reply_markup=get_enum_kb(AppointmentEnum)
        )
