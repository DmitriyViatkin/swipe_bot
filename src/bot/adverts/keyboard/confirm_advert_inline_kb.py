from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram import types


def get_confirm_advert_inline_kb():
    builder = InlineKeyboardBuilder()

    # 1 ряд: Локація та Тип
    builder.row(
        types.InlineKeyboardButton(
            text=f"📍 {_('address')}", callback_data="edit_address"
        ),
        types.InlineKeyboardButton(
            text=f"🏢 {_('appointment')}", callback_data="edit_appointment"
        ),
    )

    # 2 ряд: Характеристики будівлі
    builder.row(
        types.InlineKeyboardButton(
            text=f"📐 {_('layout')}", callback_data="edit_layout"
        ),
        types.InlineKeyboardButton(text=f"🧱 {_('state')}", callback_data="edit_state"),
    )

    # 3 ряд: Технічні деталі
    builder.row(
        types.InlineKeyboardButton(
            text=f"🔥 {_('heating')}", callback_data="edit_heating"
        ),
        types.InlineKeyboardButton(text=f"🚪 {_('rooms')}", callback_data="edit_rooms"),
    )

    # 4 ряд: Площа
    builder.row(
        types.InlineKeyboardButton(text=f"📏 {_('area')}", callback_data="edit_area"),
        types.InlineKeyboardButton(
            text=f"🍳 {_('kitchen_area')}", callback_data="edit_kitchen_area"
        ),
    )

    # 5 ряд: Умови
    builder.row(
        types.InlineKeyboardButton(
            text=f"💰 {_('payment')}", callback_data="edit_payment"
        ),
        types.InlineKeyboardButton(
            text=f"💸 {_('commission')}", callback_data="edit_commission"
        ),
    )

    # 6 ряд: Опис та Фото
    builder.row(
        types.InlineKeyboardButton(
            text=f"📝 {_('description')}", callback_data="edit_description"
        ),
        types.InlineKeyboardButton(
            text=f"🖼 {_('images')}", callback_data="edit_images"
        ),
    )

    # 7 ряд: Ціна (виділено)
    builder.row(
        types.InlineKeyboardButton(text=f"💵 {_('price')}", callback_data="edit_price")
    )

    # ФІНАЛЬНА КНОПКА
    builder.row(
        types.InlineKeyboardButton(
            text=f"✅ {_('btn_confirm_and_publish')}",
            callback_data="finish_advert_publish",
        )
    )

    return builder.as_markup()
