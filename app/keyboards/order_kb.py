from datetime import datetime
import pytz

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.callback_data import OrderCallback
from app.i18n import get_text

# Paris timezone for France
PARIS_TZ = pytz.timezone("Europe/Paris")


def is_within_working_hours() -> bool:
    """Check if current time is within working hours (Thu-Sun 13:00-19:00)"""
    now = datetime.now(PARIS_TZ)
    # weekday(): 0=Monday, 3=Thursday, 6=Sunday
    # Working days: Thursday(3), Friday(4), Saturday(5), Sunday(6)
    if now.weekday() not in [3, 4, 5, 6]:
        return False
    # Working hours: 13:00 - 19:00
    if now.hour < 13 or now.hour >= 19:
        return False
    return True


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

    # ASAP button only available during working hours
    if is_within_working_hours():
        builder.row(
            InlineKeyboardButton(
                text=f"🚀 {get_text('btn_asap', lang)}",
                callback_data="delivery_time:asap",
            )
        )

    # Custom date/time button always available
    builder.row(
        InlineKeyboardButton(
            text=f"📅 {get_text('btn_custom_time', lang)}",
            callback_data="delivery_time:custom",
        )
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
