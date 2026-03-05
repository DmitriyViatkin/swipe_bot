from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.bot.adverts.adverts_state import AdvertsState
from src.bot.adverts.keyboard.image_kb import finish_images_kb

router = Router()


@router.message(
    AdvertsState.waiting_for_price,
    F.text.regexp(r"^\d+[.,]?\d*$"),
    ~F.text.in_([__("btn_cancel_a"), __("btn_back_a")]),
)
async def price_handler(message: types.Message, state: FSMContext):

    text = message.text.replace(",", ".")

    try:
        price = float(text)
        if price <= 0:
            raise ValueError
    except ValueError:
        if message.text in [
            _("btn_skip"),
            _("btn_finish_loading"),
            _("btn_back"),
            _("btn_cancel_a"),
        ]:
            return

        await message.answer(_("enter_valid_price"))
        return

    await state.update_data(price=price)

    await state.set_state(AdvertsState.waiting_for_images)

    await message.answer(_("send_photos_now"), reply_markup=finish_images_kb())
