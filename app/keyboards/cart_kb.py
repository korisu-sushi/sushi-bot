from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.cart import Cart
from app.filters.callback_data import CartItemCallback
from app.i18n import get_text


def get_cart_keyboard(cart: Cart, lang: str = "en") -> InlineKeyboardMarkup:
    """Cart view with item controls"""
    builder = InlineKeyboardBuilder()

    # Item controls
    for item_id, item in cart.items.items():
        # Item row with quantity controls
        builder.row(
            InlineKeyboardButton(
                text="➖",
                callback_data=CartItemCallback(
                    action="dec", item_id=item_id
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f"{item.name} x{item.quantity}",
                callback_data="noop",
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data=CartItemCallback(
                    action="inc", item_id=item_id
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=CartItemCallback(
                    action="remove", item_id=item_id
                ).pack(),
            ),
        )

    # Action buttons
    builder.row(
        InlineKeyboardButton(
            text=f"🗑 {get_text('btn_clear', lang)}",
            callback_data="clear_cart",
        ),
        InlineKeyboardButton(
            text=f"✅ {get_text('btn_checkout', lang)}",
            callback_data="checkout",
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_continue_shopping', lang)}",
            callback_data="show_menu",
        )
    )

    return builder.as_markup()


def get_empty_cart_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Empty cart keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"📋 {get_text('btn_go_to_menu', lang)}",
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
