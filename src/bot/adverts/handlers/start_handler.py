from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.keyboard.control_panel import control_keyboard

router = Router()


@router.message(
    F.text == __("btn_create_advert"), ~F.text.in_([__("btn_cancel_r"), __("btn_back")])
)
async def start_create_advert(message: types.Message, state: FSMContext):

    await state.clear()

    await state.set_state(AdvertsState.waiting_for_address)
    await message.answer(_("enter_address"), reply_markup=control_keyboard())
