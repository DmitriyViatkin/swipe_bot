from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.types import URLInputFile

from src.api_client.base_api import BaseAPIClient
from .show_adverts import format_ad_text, get_advert_markup

router = Router()


@router.message(F.text == __("btn_adverts"))
async def show_adverts_list_handler(
    message: types.Message, state: FSMContext, api: BaseAPIClient
):
    res = await api.get_list_adverts()
    ads = res.get("items", [])

    if not ads:
        return await message.answer("📭 Оголошень поки немає.")

    await state.update_data(ads_cache=ads, current_ad_idx=0)

    ad = ads[0]
    gallery = ad.get("gallery") or {}
    images = gallery.get("images", [])

    photo_url = None
    if images and isinstance(images, list):
        photo_url = images[0].get("image")

    caption = format_ad_text(ad)
    markup = get_advert_markup(0, len(ads))

    if photo_url:
        try:
            photo = URLInputFile(photo_url, filename=f"ad_{ad['id']}.jpg")
            await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return
        except Exception as e:
            print(f"Фото не завантажилось: {e}")

    # без фото
    await message.answer(
        text=caption,
        reply_markup=markup,
        parse_mode="Markdown",
    )
