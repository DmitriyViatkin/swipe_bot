from aiogram import Router, F, types
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from src.api_client.base_api import BaseAPIClient
from src.bot.authorization.keyboards.auth_choise_keyboard import (
    get_auth_choice_keyboard,
)
from src.api_client.photo_utils import download_photo
from aiogram.types import BufferedInputFile

router = Router()


@router.message(F.text == __("btn_my_adverts"))
async def show_my_adverts(message: types.Message, api: BaseAPIClient):
    telegram_id = message.from_user.id
    token = api.user_tokens.get(telegram_id)

    if not token:
        return await message.answer(
            _("auth_required"), reply_markup=get_auth_choice_keyboard()
        )

    user_id = api._decode_user_id(token)
    if not user_id:
        return await message.answer(
            "❌ Не вдалось визначити ваш ID. Перезайдіть в систему."
        )

    adverts = await api.get_my_adverts(token=token, user_id=user_id)

    if isinstance(adverts, dict) and "error" in adverts:
        return await message.answer(f"❌ Помилка: {adverts['error']}")

    if not adverts:
        return await message.answer(_("no_adverts_found"))

    for adv in adverts:
        lat = adv.get("latitude")
        lon = adv.get("longitude")
        map_link = (
            f"\n📍 <a href='https://www.google.com/maps?q={lat},{lon}'>Карта</a>"
            if lat and lon
            else ""
        )

        status = "✅ Активне" if adv.get("is_active") else "❌ Неактивне"
        approved = "✅ Схвалено" if adv.get("is_approved") else "⏳ На модерації"

        caption = (
            f"🏠 <b>{adv.get('address', '—')}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🆔 ID: <code>{adv.get('id')}</code>\n"
            f"🏢 Призначення: {adv.get('appointment', '—')}\n"
            f"📐 Планування: {adv.get('layout', '—')}\n"
            f"🧱 Стан: {adv.get('state', '—')}\n"
            f"🔥 Опалення: {adv.get('heating', '—')}\n"
            f"💳 Оплата: {adv.get('payment', '—')}\n"
            f"📞 Зв'язок: {adv.get('communication', '—')}\n"
            f"🚪 Кімнат: {adv.get('rooms', '—')}\n"
            f"📏 Площа: {adv.get('area', '—')} м²\n"
            f"🍳 Кухня: {adv.get('kitchen_area', '—')} м²\n"
            f"🌅 Балкон: {'Так' if adv.get('is_balcony') else 'Ні'}\n"
            f"💸 Комісія: {adv.get('commission', '—')}\n"
            f"💵 Ціна: <b>{adv.get('price', '—')} $</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{status} | {approved}"
            f"{map_link}\n\n"
            f"📄 {adv.get('description', '—')}"
        )

        gallery = adv.get("gallery") or {}
        images = gallery.get("images", [])
        photo_url = images[0].get("image") if images else None
        print(f"PHOTO URL: {photo_url}")
        if photo_url:
            try:
                photo_bytes = await download_photo(photo_url)
                if photo_bytes:
                    filename = photo_url.split("/")[-1]
                    await message.answer_photo(
                        photo=BufferedInputFile(photo_bytes, filename=filename),
                        caption=caption,
                        parse_mode="HTML",
                    )
                    continue
            except Exception as e:
                print(f"Фото не завантажилось: {e}")

        await message.answer(text=caption, parse_mode="HTML")
