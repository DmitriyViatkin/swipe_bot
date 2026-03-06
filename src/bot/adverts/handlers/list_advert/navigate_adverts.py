from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from .show_adverts import format_ad_text, get_advert_markup
from aiogram.types import InputMediaPhoto, BufferedInputFile
from src.api_client.photo_utils import download_photo

router = Router()


@router.callback_query(F.data.in_(["next_ad", "prev_ad"]))
async def navigate_adverts_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    idx = data.get("current_ad_idx", 0)

    idx = idx + 1 if callback.data == "next_ad" else idx - 1
    last_geo_id = data.get("last_geo_msg_id")
    if last_geo_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id, message_id=last_geo_id
            )
            # Стираем ID из памяти, чтобы не пытаться удалить снова
            await state.update_data(last_geo_msg_id=None)
        except Exception:
            # Если сообщение уже удалено пользователем, просто игнорим
            pass
    # -------------------------------------

    ads = data.get("ads_cache", [])
    if idx < 0 or idx >= len(ads):
        await callback.answer()
        return

    await state.update_data(current_ad_idx=idx)
    ad = ads[idx]

    gallery = ad.get("gallery") or {}
    images = gallery.get("images", [])
    photo_url = images[0].get("image") if images else None

    caption = format_ad_text(ad)
    advert = ads[idx]

    markup = get_advert_markup(idx, len(ads), advert["id"])

    if photo_url:
        photo_bytes = await download_photo(photo_url)
        if photo_bytes:
            filename = photo_url.split("/")[-1]
            try:
                await callback.message.edit_media(
                    media=InputMediaPhoto(
                        media=BufferedInputFile(photo_bytes, filename=filename),
                        caption=caption,
                        parse_mode="Markdown",
                    ),
                    reply_markup=markup,
                )
                await callback.answer()
                return
            except Exception as e:
                print(f"Фото не завантажилось: {e}")

    try:
        await callback.message.edit_text(
            text=caption,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"edit_text помилка: {e}")

    await callback.answer()
