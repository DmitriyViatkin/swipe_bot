from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.handlers.show_summary import process_show_summary

router = Router()


@router.message(
    AdvertsState.waiting_for_images,
    F.text.in_([__("btn_finish_loading"), __("btn_skip")]),
)
async def skip_or_finish_images(message: types.Message, state: FSMContext):
    data = await state.get_data()
    images = data.get("images", [])

    await state.set_state(AdvertsState.confirm_data)

    if not images:
        await message.answer(_("images_skipped_info"))

    await process_show_summary(message, state)
