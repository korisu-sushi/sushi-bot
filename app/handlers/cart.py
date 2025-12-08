from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.filters.callback_data import CartItemCallback
from app.keyboards.cart_kb import get_cart_keyboard, get_empty_cart_keyboard
from app.services.cart_service import CartService
from app.i18n import get_text, DEFAULT_LANGUAGE
from config import settings

router = Router(name="cart")


async def get_user_lang(state: FSMContext) -> str:
    """Get user language from state"""
    data = await state.get_data()
    return data.get("lang", DEFAULT_LANGUAGE)


def format_cart_text(cart, lang: str = "en", currency: str = "₽") -> str:
    """Format cart for display"""
    if cart.is_empty:
        return get_text("cart_empty", lang)

    lines = [get_text("cart_title", lang)]

    for i, (item_id, item) in enumerate(cart.items.items(), 1):
        lines.append(
            f"{i}. {item.name} x{item.quantity} — {item.subtotal}{currency}"
        )

    lines.append(f"\n<b>{get_text('total', lang)}: {cart.total}{currency}</b>")

    # Check minimum order
    if cart.total < settings.min_order_amount:
        diff = settings.min_order_amount - cart.total
        lines.append(
            f"\n\n⚠️ {get_text('min_order_warning', lang, min_order=settings.min_order_amount, currency=currency)}"
        )
        lines.append(get_text("add_more", lang, amount=diff, currency=currency))

    return "\n".join(lines)


@router.callback_query(F.data == "show_cart")
async def show_cart(callback: CallbackQuery, state: FSMContext):
    """Show cart contents"""
    lang = await get_user_lang(state)
    cart = await CartService.get_cart(state, callback.from_user.id)

    text = format_cart_text(cart, lang)

    if cart.is_empty:
        keyboard = get_empty_cart_keyboard(lang)
    else:
        keyboard = get_cart_keyboard(cart, lang)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(CartItemCallback.filter())
async def cart_item_action(
    callback: CallbackQuery,
    callback_data: CartItemCallback,
    state: FSMContext,
):
    """Handle cart item actions (increment, decrement, remove)"""
    lang = await get_user_lang(state)
    user_id = callback.from_user.id

    if callback_data.action == "inc":
        cart = await CartService.increment_item(
            state, user_id, callback_data.item_id
        )
    elif callback_data.action == "dec":
        cart = await CartService.decrement_item(
            state, user_id, callback_data.item_id
        )
    elif callback_data.action == "remove":
        cart = await CartService.remove_item(
            state, user_id, callback_data.item_id
        )
    else:
        await callback.answer()
        return

    text = format_cart_text(cart, lang)

    if cart.is_empty:
        keyboard = get_empty_cart_keyboard(lang)
    else:
        keyboard = get_cart_keyboard(cart, lang)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    """Clear all items from cart"""
    lang = await get_user_lang(state)
    cart = await CartService.clear_cart(state, callback.from_user.id)

    await callback.message.edit_text(
        get_text("cart_cleared", lang),
        reply_markup=get_empty_cart_keyboard(lang),
    )
    await callback.answer(get_text("cart_cleared_notification", lang))
