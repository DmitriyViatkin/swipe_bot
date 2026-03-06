from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from src.bot.adverts.adverts_state import AdvertsState
from aiogram.types import ReplyKeyboardRemove
from src.bot.adverts.keyboard.confirm_advert_inline_kb import (
    get_confirm_advert_inline_kb,
)


async def process_show_summary(message: types.Message, state: FSMContext):
    await message.answer(_("send_photos_now"), reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()

    await state.set_state(AdvertsState.confirm_data)
    lat = data.get("latitude")
    lon = data.get("longitude")
    location_str = f"{lat}, {lon}" if lat and lon else _("not_specified")
    summary_text = (
        f"📝 {_('preview_advert_title')}\n\n"
        f"📍 {_('address')}: {data.get('address')}\n"
        f"🌐 {_('coordinates')}: {location_str}\n"
        f"🏢 {_('appointment')}: {data.get('appointment')}\n"
        f"📐 {_('layout')}: {data.get('layout')}\n"
        f"🧱 {_('build_state')}: {data.get('state')}\n"
        f"🔥 {_('heating')}: {data.get('heating')}\n"
        f"💰 {_('payment_type')}: {data.get('payment')}\n"
        f"📞 {_('contact')}: {data.get('communication')}\n"
        f"🚪 {_('rooms')}: {data.get('rooms')}\n"
        f"📏 {_('area')}: {data.get('area')} м2\n"
        f"🍳 {_('kitchen_area')}: {data.get('kitchen_area')} м2\n"
        f"🌅 {_('balcony')}: {'Да' if data.get('is_balcony') else 'Нет'}\n"
        f"💸 {_('commission')}: {data.get('commission')}\n"
        f"💵 {_('price')}: {data.get('price')}\n\n"
        f"🖼 {_('photos_count')}: {len(data.get('images', []))}\n"
        f"📄 {_('description')}:\n"
        f"{data.get('description')}"
    )

    await message.answer(
        text=summary_text,
        reply_markup=get_confirm_advert_inline_kb(),
        parse_mode="HTML",
    )
