from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.keyboard.enum_kb import get_enum_kb
from src.enums import HeatingEnum

router = Router()


@router.message(
    AdvertsState.waiting_for_build_state,
    ~F.text.in_([__("btn_cancel_r"), __("btn_back")]),
)
async def state_handler(message: types.Message, state: FSMContext):
    await state.update_data(state=message.text)
    await state.set_state(AdvertsState.waiting_for_heating)
    await message.answer(_("select_state"), reply_markup=get_enum_kb(HeatingEnum))
