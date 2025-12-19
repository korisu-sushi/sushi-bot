import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from app.filters.callback_data import (
    CategoryCallback,
    ItemCallback,
    QuantityCallback,
    AddToCartCallback,
)
from app.keyboards.menu_kb import (
    get_categories_keyboard,
    get_items_keyboard,
    get_item_detail_keyboard,
)
from app.services.menu_service import MenuService
from app.services.cart_service import CartService
from app.i18n import get_text, DEFAULT_LANGUAGE

router = Router(name="menu")


async def get_user_lang(state: FSMContext) -> str:
    """Get user language from state"""
    data = await state.get_data()
    return data.get("lang", DEFAULT_LANGUAGE)


@router.callback_query(F.data == "show_menu")
async def show_menu(
    callback: CallbackQuery, state: FSMContext, menu_service: MenuService
):
    """Show categories"""
    lang = await get_user_lang(state)
    menu = menu_service.get_menu()

    text = get_text("menu_title", lang)

    await callback.message.edit_text(
        text, reply_markup=get_categories_keyboard(menu, lang)
    )
    await callback.answer()


@router.callback_query(CategoryCallback.filter())
async def show_category_items(
    callback: CallbackQuery,
    callback_data: CategoryCallback,
    state: FSMContext,
    menu_service: MenuService,
):
    """Show items in category"""
    lang = await get_user_lang(state)
    category = menu_service.get_category(callback_data.category_id)
    menu = menu_service.get_menu()

    if not category:
        await callback.answer(get_text("category_not_found", lang), show_alert=True)
        return

    cart = await CartService.get_cart(state, callback.from_user.id)

    text = get_text(
        "category_title", lang, emoji=category.emoji, name=category.get_name(lang)
    )
    keyboard = get_items_keyboard(category, cart, lang, menu.currency)

    # If current message is a photo, delete and send new text message
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(ItemCallback.filter())
async def show_item_detail(
    callback: CallbackQuery,
    callback_data: ItemCallback,
    state: FSMContext,
    menu_service: MenuService,
):
    """Show item details"""
    lang = await get_user_lang(state)
    item = menu_service.get_item(callback_data.item_id)
    menu = menu_service.get_menu()

    if not item:
        await callback.answer(get_text("item_not_found", lang), show_alert=True)
        return

    category = menu_service.get_category_for_item(item.id)
    category_id = category.id if category else ""

    # Get current quantity in cart
    cart = await CartService.get_cart(state, callback.from_user.id)
    current_qty = 1
    if item.id in cart.items:
        current_qty = cart.items[item.id].quantity

    # Store current quantity in state for increment/decrement
    await state.update_data(
        viewing_item_id=item.id,
        viewing_item_qty=1,
        viewing_category_id=category_id,
    )

    # Build item description
    text = get_text(
        "item_detail",
        lang,
        name=item.get_name(lang),
        description=item.get_description(lang),
        weight=item.weight,
        pieces=f" | {item.pieces} {get_text('pcs', lang)}" if item.pieces else "",
        price=item.price,
        currency=menu.currency,
        popular=f"\n\n⭐ {get_text('popular_item', lang)}" if item.popular else "",
    )

    keyboard = get_item_detail_keyboard(
        item, quantity=1, category_id=category_id, lang=lang, currency=menu.currency
    )

    # Check if item has image
    if item.image and os.path.exists(item.image):
        # Delete old message and send photo
        await callback.message.delete()
        photo = FSInputFile(item.image)
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(QuantityCallback.filter())
async def change_quantity(
    callback: CallbackQuery,
    callback_data: QuantityCallback,
    state: FSMContext,
    menu_service: MenuService,
):
    """Handle quantity change"""
    lang = await get_user_lang(state)
    item = menu_service.get_item(callback_data.item_id)
    menu = menu_service.get_menu()

    if not item:
        await callback.answer(get_text("item_not_found", lang), show_alert=True)
        return

    # Get current state
    data = await state.get_data()
    current_qty = data.get("viewing_item_qty", 1)
    category_id = data.get("viewing_category_id", "")

    # Calculate new quantity
    if callback_data.action == "inc":
        new_qty = min(current_qty + 1, 99)  # Max 99
    else:
        new_qty = max(current_qty - 1, 1)  # Min 1

    # Update state
    await state.update_data(viewing_item_qty=new_qty)

    # Build item description
    text = get_text(
        "item_detail",
        lang,
        name=item.get_name(lang),
        description=item.get_description(lang),
        weight=item.weight,
        pieces=f" | {item.pieces} {get_text('pcs', lang)}" if item.pieces else "",
        price=item.price,
        currency=menu.currency,
        popular=f"\n\n⭐ {get_text('popular_item', lang)}" if item.popular else "",
    )

    keyboard = get_item_detail_keyboard(
        item, quantity=new_qty, category_id=category_id, lang=lang, currency=menu.currency
    )

    # Check if current message is a photo (has caption)
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard,
        )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
        )
    await callback.answer()


@router.callback_query(AddToCartCallback.filter())
async def add_to_cart(
    callback: CallbackQuery,
    callback_data: AddToCartCallback,
    state: FSMContext,
    menu_service: MenuService,
):
    """Add item to cart"""
    lang = await get_user_lang(state)
    item = menu_service.get_item(callback_data.item_id)
    menu = menu_service.get_menu()

    if not item:
        await callback.answer(get_text("item_not_found", lang), show_alert=True)
        return

    # Get quantity from state (set by quantity buttons)
    data = await state.get_data()
    quantity = data.get("viewing_item_qty", callback_data.quantity)

    # Add to cart
    cart = await CartService.add_item(
        state, callback.from_user.id, item, quantity, lang
    )

    # Show confirmation and return to category
    category = menu_service.get_category_for_item(item.id)

    await callback.answer(
        get_text("added_to_cart", lang, name=item.get_name(lang), quantity=quantity),
        show_alert=False,
    )

    if category:
        text = get_text(
            "category_title", lang, emoji=category.emoji, name=category.get_name(lang)
        )
        keyboard = get_items_keyboard(category, cart, lang, menu.currency)

        # If current message is a photo, delete and send new text message
        if callback.message.photo:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=keyboard)
        else:
            await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        # Fallback to categories
        text = get_text("menu_title", lang)
        keyboard = get_categories_keyboard(menu, lang)

        if callback.message.photo:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=keyboard)
        else:
            await callback.message.edit_text(text, reply_markup=keyboard)
