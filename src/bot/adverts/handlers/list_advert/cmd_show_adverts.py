from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.types import URLInputFile  # Импортируем для стабильности

from src.api_client.base_api import BaseAPIClient
from .show_adverts import DEFAULT_IMAGE, format_ad_text, get_advert_markup

router = Router()


@router.message(F.text == __("btn_adverts"))
async def show_adverts_list_handler(
    message: types.Message, state: FSMContext, api: BaseAPIClient
):
    res = await api.get_list_adverts()
    ads = res.get("items", [])

    if not ads:
        return await message.answer(_("📭 Оголошень поки немає."))

    # Сохраняем в кэш
    await state.update_data(ads_cache=ads, current_ad_idx=0)

    ad = ads[0]
    gallery = ad.get("gallery") or {}
    images = gallery.get("images", [])

    # Определяем URL
    if images and isinstance(images, list) and len(images) > 0:
        image_url = images[0].get("image") or DEFAULT_IMAGE
    else:
        image_url = DEFAULT_IMAGE

    try:
        # Пытаемся отправить через URLInputFile (более надежно для Telegram)
        # Если ссылка рабочая, aiogram сам ее подхватит
        photo = URLInputFile(image_url, filename=f"ad_{ad['id']}.jpg")

        await message.answer_photo(
            photo=photo,
            caption=format_ad_text(ad),
            reply_markup=get_advert_markup(0, len(ads)),
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Ошибка отправки фото ({image_url}): {e}")
        # Если не вышло — отправляем текст
        await message.answer(
            text="🖼 *(Фото не завантажилось)*\n\n" + format_ad_text(ad),
            reply_markup=get_advert_markup(0, len(ads)),
            parse_mode="Markdown",
        )
