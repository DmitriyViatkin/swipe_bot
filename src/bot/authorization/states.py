from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()


class RegistrationState(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()

    waiting_for_photo = State()
    waiting_for_password = State()
    confirm_data = State()
