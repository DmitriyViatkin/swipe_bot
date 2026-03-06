from aiogram.fsm.state import StatesGroup, State


class AdvertsState(StatesGroup):
    waiting_for_address = State()
    waiting_for_location = State()
    waiting_for_appointment = State()
    waiting_for_layout = State()
    waiting_for_build_state = State()
    waiting_for_heating = State()
    waiting_for_payment = State()
    waiting_for_communication = State()
    waiting_for_rooms = State()
    waiting_for_area = State()
    waiting_for_kitchen_area = State()
    waiting_for_is_balcony = State()
    waiting_for_commission = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_images = State()
    confirm_data = State()
