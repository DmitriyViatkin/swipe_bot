from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..adverts_state import AdvertsState
from src.enums import AppointmentEnum
from ..keyboard.enum_kb import get_enum_kb
from aiogram.utils.i18n import gettext as _
from ..handlers.show_summary import process_show_summary
import re

router = Router()


@router.message(
    AdvertsState.waiting_for_location
)  # Убрали F.location отсюда, чтобы ловить и текст
async def location_handler(message: types.Message, state: FSMContext):
    lat, lon = None, None

    # 1. Если пользователь прислал геолокацию кнопкой
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude

    # 2. Если пользователь ввел координаты текстом (например: "50.45, 30.52")
    elif message.text:
        try:
            # Ищем числа в строке (поддерживает пробелы, запятые и точки)
            coords = re.findall(r"[-+]?\d*\.\d+|\d+", message.text)
            if len(coords) >= 2:
                lat = float(coords[0])
                lon = float(coords[1])
            else:
                return await message.answer(
                    _("invalid_coords_format")
                )  # "Формат неверный. Введите: лат, лон"
        except ValueError:
            return await message.answer(_("invalid_coords_values"))

    # Если ничего не подошло
    if lat is None or lon is None:
        return await message.answer(_("send_location_or_text"))

    # Сохраняем данные
    await state.update_data(latitude=lat, longitude=lon)

    # Твоя логика редактирования или перехода к следующему шагу
    data = await state.get_data()
    if data.get("is_editing"):
        await state.update_data(is_editing=False, edit_field=None)
        await state.set_state(AdvertsState.confirm_data)
        await process_show_summary(message, state)
    else:
        await state.set_state(AdvertsState.waiting_for_appointment)
        await message.answer(
            _("select_appointment"), reply_markup=get_enum_kb(AppointmentEnum)
        )
