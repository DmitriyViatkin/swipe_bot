from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data.startswith("show_geo:"))
async def show_geo_handler(callback: types.CallbackQuery, state: FSMContext):
    advert_id = int(callback.data.split(":")[1])

    data = await state.get_data()
    ads = data.get("ads_cache", [])

    ad = next((a for a in ads if a["id"] == advert_id), None)

    if not ad:
        return await callback.answer("Оголошення не знайдено", show_alert=True)

    lat = ad.get("latitude")
    lon = ad.get("longitude")

    if not lat or not lon:
        return await callback.answer("📍 Локація не вказана", show_alert=True)

    lat = float(lat)
    lon = float(lon)

    await callback.message.answer_location(latitude=lat, longitude=lon)
    await callback.answer()
