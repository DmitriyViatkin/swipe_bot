from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from .show_adverts import DEFAULT_IMAGE, format_ad_text, get_advert_markup
from aiogram.types import InputMediaPhoto, URLInputFile

router = Router()


@router.callback_query(F.data.in_(["next_ad", "prev_ad"]))
async def navigate_adverts_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ads = data.get("ads_cache", [])
    idx = data.get("current_ad_idx", 0)

    idx = idx + 1 if callback.data == "next_ad" else idx - 1

    if idx < 0 or idx >= len(ads):
        await callback.answer()
        return

    await state.update_data(current_ad_idx=idx)
    ad = ads[idx]

    gallery = ad.get("gallery") or {}
    images = gallery.get("images", [])
    image_url = images[0].get("image") if images else DEFAULT_IMAGE

    try:
        # 1. Пробуем обновить медиа
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=URLInputFile(image_url, filename=f"ad_{ad['id']}.jpg"),
                caption=format_ad_text(ad),
                parse_mode="Markdown",
            ),
            reply_markup=get_advert_markup(idx, len(ads)),
        )
    except Exception as e:
        print(f"DEBUG: Ошибка обновления медиа: {e}")
        # 2. Если не вышло (wrong type или нет текста), удаляем старое и шлем новое
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=URLInputFile(image_url, filename=f"ad_{ad['id']}.jpg"),
            caption=format_ad_text(ad),
            reply_markup=get_advert_markup(idx, len(ads)),
            parse_mode="Markdown",
        )

    await callback.answer()
