from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.adverts.adverts_state import AdvertsState

router = Router()


@router.callback_query(AdvertsState.confirm_data, F.data.startswith("edit_"))
async def edit_advert_field(callback: types.CallbackQuery, state: FSMContext):
    field_to_edit = callback.data.replace("edit_", "")

    states_map = {
        "address": AdvertsState.waiting_for_address,
        "appointment": AdvertsState.waiting_for_appointment,
        "layout": AdvertsState.waiting_for_layout,
        "state": AdvertsState.waiting_for_build_state,
        "heating": AdvertsState.waiting_for_heating,
        "payment": AdvertsState.waiting_for_payment,
        "communication": AdvertsState.waiting_for_communication,
        "rooms": AdvertsState.waiting_for_rooms,
        "area": AdvertsState.waiting_for_area,
        "kitchen_area": AdvertsState.waiting_for_kitchen_area,
        "balcony": AdvertsState.waiting_for_is_balcony,
        "commission": AdvertsState.waiting_for_commission,
        "description": AdvertsState.waiting_for_description,
        "price": AdvertsState.waiting_for_price,
        "images": AdvertsState.waiting_for_images,
    }

    new_state = states_map.get(field_to_edit)

    if new_state:
        await state.update_data(is_editing=True, edit_field=field_to_edit)

        await state.set_state(new_state)

        await callback.message.answer(f"🔄 {_('edit_mode_on')}: {_(field_to_edit)}")

        await callback.message.answer(_(f"enter_{field_to_edit}"))
        await callback.answer()
    else:
        await callback.answer("Error: field not mapped", show_alert=True)
