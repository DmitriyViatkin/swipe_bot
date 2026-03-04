from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from ..adverts_state import AdvertsState
from aiogram.fsm.context import FSMContext
from ..handlers.show_summary import process_show_summary

router = Router()


@router.message(AdvertsState.waiting_for_images, F.text == __("btn_finish_loading"))
async def finish_loading_photos(message: types.Message, state: FSMContext):

    data = await state.get_data()
    images = data.get("images", [])

    if not images:
        await message.answer(_("error_no_photos"))
        return

    await state.update_data(is_editing=False, edit_field=None)

    await state.set_state(AdvertsState.confirm_data)

    await process_show_summary(message, state)
