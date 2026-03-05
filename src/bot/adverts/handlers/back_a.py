from src.enums import (
    AppointmentEnum,
    LayoutEnum,
    StateEnum,
    PaymentEnum,
    HeatingEnum,
    CommunicationPartyEnum,
)
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from ..adverts_state import AdvertsState
from ..keyboard.enum_kb import get_enum_kb
from ..keyboard.control_panel import control_keyboard


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
    AdvertsState.waiting_for_heating: (
        AdvertsState.waiting_for_build_state,  # Исправлено (было layout)
        "select_state",
        StateEnum,
    ),
    AdvertsState.waiting_for_payment: (
        AdvertsState.waiting_for_heating,
        "select_heating",
        HeatingEnum,
    ),
    AdvertsState.waiting_for_communication: (
        AdvertsState.waiting_for_payment,
        "select_payment",
        PaymentEnum,
    ),
    AdvertsState.waiting_for_rooms: (
        AdvertsState.waiting_for_communication,
        "select_communication",
        CommunicationPartyEnum,
    ),
    AdvertsState.waiting_for_area: (
        AdvertsState.waiting_for_rooms,
        "enter_rooms",
        None,
    ),
    AdvertsState.waiting_for_kitchen_area: (
        AdvertsState.waiting_for_area,
        "enter_area",
        None,
    ),
    AdvertsState.waiting_for_is_balcony: (
        AdvertsState.waiting_for_kitchen_area,
        "enter_area_kitchen",
        None,
    ),
    AdvertsState.waiting_for_commission: (
        AdvertsState.waiting_for_is_balcony,
        "is_there_balcony",
        None,
    ),
    AdvertsState.waiting_for_description: (
        AdvertsState.waiting_for_commission,
        "enter_commission",
        None,
    ),
    AdvertsState.waiting_for_price: (
        AdvertsState.waiting_for_description,
        "enter_description",
        None,
    ),
    AdvertsState.waiting_for_images: (
        AdvertsState.waiting_for_price,
        "enter_price",
        None,
    ),
}

STATES_MAP_STR = {s.state: v for s, v in STATES_MAP.items()}


@router.message(F.text == __("btn_back_a"))
async def back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state in STATES_MAP_STR:
        prev_state, text_key, enum_class = STATES_MAP[current_state]

        await state.set_state(prev_state)

        kb = None
        if enum_class:
            kb = get_enum_kb(enum_class)
        else:
            kb = control_keyboard()

        await message.answer(_(text_key), reply_markup=kb)
