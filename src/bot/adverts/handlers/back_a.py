from src.enums import AppointmentEnum, LayoutEnum
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from ..adverts_state import AdvertsState
from ..keyboard.enum_kb import get_enum_kb


router = Router()

STATES_MAP = {
    AdvertsState.waiting_for_appointment: (
        AdvertsState.waiting_for_address,
        "enter_address",
        None,
    ),
    AdvertsState.waiting_for_layout: (
        AdvertsState.waiting_for_appointment,
        "select_appointment",
        AppointmentEnum,
    ),
    AdvertsState.waiting_for_build_state: (
        AdvertsState.waiting_for_layout,
        "select_layout",
        LayoutEnum,
    ),
}


@router.message(F.text == __("btn_back"))
async def back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state in STATES_MAP:
        prev_state, text_key, enum_class = STATES_MAP[current_state]

        await state.set_state(prev_state)

        # Создаем клавиатуру ТОЛЬКО ЗДЕСЬ
        kb = None
        if enum_class:
            kb = get_enum_kb(enum_class)

        await message.answer(
            _(text_key), reply_markup=kb if kb else types.ReplyKeyboardRemove()
        )
