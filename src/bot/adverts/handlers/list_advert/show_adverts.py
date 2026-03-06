from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


router = Router()

DEFAULT_IMAGE = "https://via.placeholder.com/800x600.png?text=No+Photo"


def get_advert_markup(current_index: int, total_count: int, advert_id: int):
    buttons = []
    # Кнопка локации (пока заглушка)
    buttons.append(
        [
            InlineKeyboardButton(
                text=_("📍 Локація"), callback_data=f"show_geo:{advert_id}"
            )
        ]
    )

    nav_row = []
    # Кнопка "Назад" (только если мы не на первом объявлении)
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data="prev_ad"))

    nav_row.append(
        InlineKeyboardButton(
            text=f"{current_index + 1}/{total_count}", callback_data="ignore"
        )
    )

    # Кнопка "Вперед" (только если есть куда листать)
    if current_index < total_count - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data="next_ad"))

    if nav_row:
        buttons.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_ad_text(ad: dict):

    try:
        price = f"{float(ad.get('price', 0)):,.0f}".replace(",", " ")
    except (ValueError, TypeError):
        price = ad.get("price", 0)

    return (
        f" **{ad.get('appointment', _('Нерухомість'))}**\n"
        f" Адреса: `{ad.get('address', '---')}`\n"
        f" Ціна: **{price} грн**\n"
        f" Кімнат: {ad.get('rooms', 0)} |  {ad.get('area', 0)} м²\n"
        f" Опалення: {ad.get('heating') or _('Не вказано')}\n"
        f" Стан: {ad.get('state') or _('Не вказано')}\n"
        f"---------------------------\n"
        f" {ad.get('description') or _('Без опису')}"
    )
