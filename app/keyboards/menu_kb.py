from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.menu import Menu, Category, MenuItem
from app.models.cart import Cart
from app.filters.callback_data import (
    CategoryCallback,
    ItemCallback,
    AddToCartCallback,
    QuantityCallback,
)
from app.i18n import get_text, LANGUAGES


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"{LANGUAGES['en']['flag']} {LANGUAGES['en']['name']}",
            callback_data="set_lang:en",
        ),
        InlineKeyboardButton(
            text=f"{LANGUAGES['fr']['flag']} {LANGUAGES['fr']['name']}",
            callback_data="set_lang:fr",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{LANGUAGES['uk']['flag']} {LANGUAGES['uk']['name']}",
            callback_data="set_lang:uk",
        ),
        InlineKeyboardButton(
            text=f"{LANGUAGES['ru']['flag']} {LANGUAGES['ru']['name']}",
            callback_data="set_lang:ru",
        ),
    )

    return builder.as_markup()


def get_main_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Main menu with primary actions"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"📋 {get_text('btn_menu', lang)}",
            callback_data="show_menu",
        ),
        InlineKeyboardButton(
            text=f"🛒 {get_text('btn_cart', lang)}",
            callback_data="show_cart",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"📞 {get_text('btn_contacts', lang)}",
            callback_data="show_contacts",
        ),
        InlineKeyboardButton(
            text=f"❓ {get_text('btn_help', lang)}",
            callback_data="show_help",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"🌐 {get_text('btn_language', lang)}",
            callback_data="change_language",
        )
    )

    return builder.as_markup()


def get_categories_keyboard(menu: Menu, lang: str = "en") -> InlineKeyboardMarkup:
    """Category selection keyboard"""
    builder = InlineKeyboardBuilder()

    for category in menu.get_sorted_categories():
        available_count = len(category.get_available_items())
        if available_count > 0:
            builder.row(
                InlineKeyboardButton(
                    text=f"{category.emoji} {category.get_name(lang)} ({available_count})",
                    callback_data=CategoryCallback(
                        category_id=category.id
                    ).pack(),
                )
            )

    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_main_menu', lang)}",
            callback_data="main_menu",
        )
    )

    return builder.as_markup()


def get_items_keyboard(
    category: Category,
    cart: Cart | None = None,
    lang: str = "en",
    currency: str = "€",
) -> InlineKeyboardMarkup:
    """Items list in category"""
    builder = InlineKeyboardBuilder()

    for item in category.get_available_items():
        # Check if item is in cart
        cart_qty = ""
        if cart and item.id in cart.items:
            cart_qty = f" ✓{cart.items[item.id].quantity}"

        builder.row(
            InlineKeyboardButton(
                text=f"{item.get_name(lang)} — {item.price}{currency}{cart_qty}",
                callback_data=ItemCallback(item_id=item.id).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=f"◀️ {get_text('btn_back_categories', lang)}",
            callback_data="show_menu",
        )
    )

    # Add cart button if cart has items
    if cart and not cart.is_empty:
        builder.row(
            InlineKeyboardButton(
                text=f"🛒 {get_text('btn_cart', lang)} ({cart.item_count})",
                callback_data="show_cart",
            )
        )

    return builder.as_markup()


def get_item_detail_keyboard(
    item: MenuItem,
    quantity: int = 1,
    category_id: str = "",
    lang: str = "en",
    currency: str = "€",
) -> InlineKeyboardMarkup:
    """Item detail with quantity selector"""
    builder = InlineKeyboardBuilder()

    # Quantity selector row
    builder.row(
        InlineKeyboardButton(
            text="➖",
            callback_data=QuantityCallback(
                item_id=item.id, action="dec", current=quantity
            ).pack(),
        ),
        InlineKeyboardButton(text=f"  {quantity}  ", callback_data="noop"),
        InlineKeyboardButton(
            text="➕",
            callback_data=QuantityCallback(
                item_id=item.id, action="inc", current=quantity
            ).pack(),
        ),
    )

    # Add to cart button
    total = item.price * quantity
    builder.row(
        InlineKeyboardButton(
            text=f"🛒 {get_text('btn_add_to_cart', lang)} — {total}{currency}",
            callback_data=AddToCartCallback(
                item_id=item.id, quantity=quantity
            ).pack(),
        )
    )

    # Back button
    if category_id:
        builder.row(
            InlineKeyboardButton(
                text=f"◀️ {get_text('btn_back', lang)}",
                callback_data=CategoryCallback(category_id=category_id).pack(),
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text=f"◀️ {get_text('btn_back', lang)}",
                callback_data="show_menu",
            )
        )

    return builder.as_markup()
