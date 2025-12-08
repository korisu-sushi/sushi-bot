from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.callback_data import OrderCallback
from app.i18n import get_text


def get_delivery_type_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Delivery type selection"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"🚗 {get_text('btn_delivery', lang)}",
            callback_data="delivery_type:delivery",
        ),
        InlineKeyboardButton(
            text=f"🏪 {get_text('btn_pickup', lang)}",
            callback_data="delivery_type:pickup",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_back_to_cart', lang)}",
            callback_data="show_cart",
        )
    )

    return builder.as_markup()


def get_delivery_time_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Delivery time selection"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"🚀 {get_text('btn_asap', lang)}",
            callback_data="delivery_time:asap",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"🕐 {get_text('btn_in_1_hour', lang)}",
            callback_data="delivery_time:1h",
        ),
        InlineKeyboardButton(
            text=f"🕑 {get_text('btn_in_2_hours', lang)}",
            callback_data="delivery_time:2h",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_back', lang)}",
            callback_data="order_back",
        )
    )

    return builder.as_markup()


def get_skip_comment_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Skip comment keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"⏭ {get_text('btn_skip', lang)}",
            callback_data="skip_comment",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_back', lang)}",
            callback_data="order_back",
        )
    )

    return builder.as_markup()


def get_confirm_order_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Order confirmation keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"✅ {get_text('btn_confirm_order', lang)}",
            callback_data=OrderCallback(action="confirm").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"❌ {get_text('btn_cancel', lang)}",
            callback_data=OrderCallback(action="cancel").pack(),
        )
    )

    return builder.as_markup()


def get_order_complete_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Post-order keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"📋 {get_text('btn_new_order', lang)}",
            callback_data="show_menu",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_main_menu', lang)}",
            callback_data="main_menu",
        )
    )

    return builder.as_markup()
