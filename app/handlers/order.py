import re
from datetime import date
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.order_states import OrderState
from app.filters.callback_data import OrderCallback, DaySelectionCallback, TimeSlotCallback
from app.keyboards.order_kb import (
    get_delivery_type_keyboard,
    get_day_selection_keyboard,
    get_time_slot_keyboard,
    get_skip_comment_keyboard,
    get_confirm_order_keyboard,
    get_order_complete_keyboard,
    format_delivery_time,
    format_date_label,
    PARIS_TZ,
)
from app.keyboards.cart_kb import get_cart_keyboard
from app.services.cart_service import CartService
from app.services.sheets_service import GoogleSheetsService
from app.services.notification_service import NotificationService
from app.models.order import Order, DeliveryType
from app.i18n import get_text, DEFAULT_LANGUAGE
from config import settings
from datetime import datetime

router = Router(name="order")


async def get_user_lang(state: FSMContext) -> str:
    """Get user language from state"""
    data = await state.get_data()
    return data.get("lang", DEFAULT_LANGUAGE)


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove spaces, dashes, parentheses, dots
    cleaned = re.sub(r"[\s\-\(\)\.]", "", phone)
    # French format: +33XXXXXXXXX or 0XXXXXXXXX (9-10 digits after prefix)
    # International format: +XXXXXXXXXXX (10-15 digits)
    if re.match(r"^(\+33|0033|0)\d{9}$", cleaned):
        return True
    if re.match(r"^\+\d{10,15}$", cleaned):
        return True
    # Simple 10 digit number
    if re.match(r"^\d{10}$", cleaned):
        return True
    return False


def format_order_summary(
    cart,
    customer_name: str,
    customer_phone: str,
    delivery_type: DeliveryType,
    delivery_address: str | None,
    delivery_time: str,
    comment: str | None,
    delivery_fee: int,
    lang: str = "en",
    currency: str = "€",
) -> str:
    """Format order for confirmation"""
    lines = [
        get_text("order_confirmation_title", lang),
        f"👤 {get_text('name', lang)}: {customer_name}",
        f"📞 {get_text('phone', lang)}: {customer_phone}",
        f"🚗 {get_text('type', lang)}: {get_text('delivery' if delivery_type == DeliveryType.DELIVERY else 'pickup', lang)}",
    ]

    if delivery_address:
        lines.append(f"📍 {get_text('address', lang)}: {delivery_address}")

    lines.append(f"🕐 {get_text('time', lang)}: {delivery_time}")

    if comment:
        lines.append(f"💬 {get_text('comment', lang)}: {comment}")

    lines.append(f"\n<b>{get_text('order', lang)}:</b>")

    for item in cart.items.values():
        lines.append(f"• {item.name} x{item.quantity} — {item.subtotal}{currency}")

    lines.append(f"\n{get_text('subtotal', lang)}: {cart.total}{currency}")

    if delivery_fee > 0:
        lines.append(f"{get_text('delivery_fee', lang)}: {delivery_fee}{currency}")
        lines.append(f"\n<b>{get_text('total', lang)}: {cart.total + delivery_fee}{currency}</b>")
    else:
        lines.append(f"\n<b>{get_text('total', lang)}: {cart.total}{currency}</b>")

    return "\n".join(lines)


@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    """Start checkout process"""
    lang = await get_user_lang(state)
    cart = await CartService.get_cart(state, callback.from_user.id)

    if cart.is_empty:
        await callback.answer(get_text("cart_is_empty", lang), show_alert=True)
        return

    if cart.total < settings.min_order_amount:
        await callback.answer(
            get_text("min_order_alert", lang, amount=settings.min_order_amount, currency="€"),
            show_alert=True,
        )
        return

    await state.set_state(OrderState.waiting_for_name)

    await callback.message.edit_text(get_text("enter_name", lang))
    await callback.answer()


@router.message(OrderState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Process customer name"""
    lang = await get_user_lang(state)
    name = message.text.strip()

    if len(name) < 2:
        await message.answer(get_text("name_too_short", lang))
        return

    if len(name) > 50:
        await message.answer(get_text("name_too_long", lang))
        return

    await state.update_data(customer_name=name)
    await state.set_state(OrderState.waiting_for_phone)

    await message.answer(get_text("enter_phone", lang))


@router.message(OrderState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Process customer phone"""
    lang = await get_user_lang(state)
    phone = message.text.strip()

    if not validate_phone(phone):
        await message.answer(get_text("invalid_phone", lang))
        return

    await state.update_data(customer_phone=phone)
    await state.set_state(OrderState.waiting_for_address)

    await message.answer(
        get_text("choose_delivery_type", lang),
        reply_markup=get_delivery_type_keyboard(lang),
    )


@router.callback_query(F.data.startswith("delivery_type:"))
async def process_delivery_type(callback: CallbackQuery, state: FSMContext):
    """Process delivery type selection"""
    lang = await get_user_lang(state)
    delivery_type = callback.data.split(":")[1]

    if delivery_type == "pickup":
        # Pickup - skip address, go to day selection
        await state.update_data(
            delivery_type=DeliveryType.PICKUP,
            delivery_address=None,
            delivery_fee=0,
        )
        await state.set_state(OrderState.waiting_for_delivery_day)

        await callback.message.edit_text(
            get_text("select_delivery_day", lang),
            reply_markup=get_day_selection_keyboard(lang),
        )
    else:
        # Delivery - ask for address
        await state.update_data(delivery_type=DeliveryType.DELIVERY)
        await state.set_state(OrderState.waiting_for_address)

        await callback.message.edit_text(get_text("enter_address", lang))

    await callback.answer()


@router.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    """Process delivery address"""
    lang = await get_user_lang(state)
    address = message.text.strip()

    if len(address) < 5:
        await message.answer(get_text("address_too_short", lang))
        return

    # Delivery fee is always charged for delivery orders
    delivery_fee = settings.delivery_fee

    await state.update_data(delivery_address=address, delivery_fee=delivery_fee)
    await state.set_state(OrderState.waiting_for_delivery_day)

    fee_text = ""
    if delivery_fee > 0:
        fee_text = f"\n\n{get_text('delivery_cost', lang, fee=delivery_fee, threshold=settings.free_delivery_threshold, currency='€')}"

    await message.answer(
        f"{get_text('select_delivery_day', lang)}{fee_text}",
        reply_markup=get_day_selection_keyboard(lang),
    )


@router.callback_query(DaySelectionCallback.filter())
async def process_day_selection(callback: CallbackQuery, callback_data: DaySelectionCallback, state: FSMContext):
    """Process delivery day selection"""
    lang = await get_user_lang(state)

    # Parse the selected date
    selected_date = date.fromisoformat(callback_data.day)
    today = datetime.now(PARIS_TZ).date()

    # Format date for display
    date_label = format_date_label(selected_date, lang, today)

    # Save selected day
    await state.update_data(selected_date=callback_data.day)
    await state.set_state(OrderState.waiting_for_time_slot)

    await callback.message.edit_text(
        get_text("select_time_slot", lang, date=date_label),
        reply_markup=get_time_slot_keyboard(selected_date, lang),
    )
    await callback.answer()


@router.callback_query(TimeSlotCallback.filter())
async def process_time_slot_selection(callback: CallbackQuery, callback_data: TimeSlotCallback, state: FSMContext):
    """Process time slot selection"""
    lang = await get_user_lang(state)
    data = await state.get_data()

    # Get saved date
    selected_date = date.fromisoformat(data["selected_date"])
    time_slot = callback_data.time

    # Format delivery time for display
    delivery_time = format_delivery_time(selected_date, time_slot, lang)

    await state.update_data(delivery_time=delivery_time)
    await state.set_state(OrderState.waiting_for_comment)

    await callback.message.edit_text(
        get_text("enter_comment", lang),
        reply_markup=get_skip_comment_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "skip_comment")
async def skip_comment(callback: CallbackQuery, state: FSMContext):
    """Skip comment and proceed to confirmation"""
    await state.update_data(comment=None)
    await show_confirmation(callback, state)


@router.message(OrderState.waiting_for_comment)
async def process_comment(message: Message, state: FSMContext):
    """Process order comment"""
    lang = await get_user_lang(state)
    comment = message.text.strip()

    if len(comment) > 500:
        await message.answer(
            get_text("comment_too_long", lang),
            reply_markup=get_skip_comment_keyboard(lang),
        )
        return

    await state.update_data(comment=comment)

    # Show confirmation
    await state.set_state(OrderState.confirmation)

    cart = await CartService.get_cart(state, message.from_user.id)
    data = await state.get_data()

    summary = format_order_summary(
        cart=cart,
        customer_name=data["customer_name"],
        customer_phone=data["customer_phone"],
        delivery_type=data["delivery_type"],
        delivery_address=data.get("delivery_address"),
        delivery_time=data["delivery_time"],
        comment=comment,
        delivery_fee=data.get("delivery_fee", 0),
        lang=lang,
    )

    await message.answer(summary, reply_markup=get_confirm_order_keyboard(lang))


async def show_confirmation(callback: CallbackQuery, state: FSMContext):
    """Show order confirmation"""
    lang = await get_user_lang(state)
    await state.set_state(OrderState.confirmation)

    cart = await CartService.get_cart(state, callback.from_user.id)
    data = await state.get_data()

    summary = format_order_summary(
        cart=cart,
        customer_name=data["customer_name"],
        customer_phone=data["customer_phone"],
        delivery_type=data["delivery_type"],
        delivery_address=data.get("delivery_address"),
        delivery_time=data["delivery_time"],
        comment=data.get("comment"),
        delivery_fee=data.get("delivery_fee", 0),
        lang=lang,
    )

    await callback.message.edit_text(
        summary, reply_markup=get_confirm_order_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "order_back")
async def order_back(callback: CallbackQuery, state: FSMContext):
    """Go back in order flow"""
    lang = await get_user_lang(state)
    current_state = await state.get_state()
    data = await state.get_data()

    if current_state == OrderState.waiting_for_delivery_day:
        # Go back based on delivery type
        if data.get("delivery_type") == DeliveryType.PICKUP:
            # Go back to delivery type selection
            await state.set_state(OrderState.waiting_for_address)
            await callback.message.edit_text(
                get_text("choose_delivery_type", lang),
                reply_markup=get_delivery_type_keyboard(lang),
            )
        else:
            # Go back to address input
            await state.set_state(OrderState.waiting_for_address)
            await callback.message.edit_text(get_text("enter_address", lang))

    elif current_state == OrderState.waiting_for_time_slot:
        # Go back to day selection
        await state.set_state(OrderState.waiting_for_delivery_day)
        await callback.message.edit_text(
            get_text("select_delivery_day", lang),
            reply_markup=get_day_selection_keyboard(lang),
        )

    elif current_state == OrderState.waiting_for_comment:
        # Go back to time slot selection
        selected_date = date.fromisoformat(data["selected_date"])
        today = datetime.now(PARIS_TZ).date()
        date_label = format_date_label(selected_date, lang, today)

        await state.set_state(OrderState.waiting_for_time_slot)
        await callback.message.edit_text(
            get_text("select_time_slot", lang, date=date_label),
            reply_markup=get_time_slot_keyboard(selected_date, lang),
        )

    else:
        # Default - back to cart
        cart = await CartService.get_cart(state, callback.from_user.id)
        from app.handlers.cart import format_cart_text

        # Keep language when clearing state
        await state.clear()
        await state.update_data(lang=lang)
        await callback.message.edit_text(
            format_cart_text(cart, lang),
            reply_markup=get_cart_keyboard(cart, lang),
        )

    await callback.answer()


@router.callback_query(OrderCallback.filter(F.action == "confirm"))
async def confirm_order(
    callback: CallbackQuery,
    state: FSMContext,
    sheets_service: GoogleSheetsService,
    notification_service: NotificationService,
):
    """Confirm and save order"""
    lang = await get_user_lang(state)
    cart = await CartService.get_cart(state, callback.from_user.id)

    if cart.is_empty:
        await callback.answer(get_text("cart_is_empty", lang), show_alert=True)
        return

    data = await state.get_data()

    # Generate order ID
    order_id = await sheets_service.get_next_order_id()

    # Create order
    order = Order.from_cart(
        order_id=order_id,
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        customer_name=data["customer_name"],
        customer_phone=data["customer_phone"],
        delivery_type=data["delivery_type"],
        delivery_address=data.get("delivery_address"),
        delivery_time=data["delivery_time"],
        cart_items=cart.items,
        delivery_fee=data.get("delivery_fee", 0),
        comment=data.get("comment"),
    )

    # Save to Google Sheets
    saved = await sheets_service.save_order(order)

    # Send notification to kitchen channel
    notified = await notification_service.send_order_notification(order)

    # Clear cart and state, but keep language
    await CartService.clear_cart(state, callback.from_user.id)
    await state.clear()
    await state.update_data(lang=lang)

    # Show success message
    save_note = ""
    if not saved and not notified:
        save_note = f"\n\n<i>⚠️ {get_text('order_manual_processing', lang)}</i>"

    success_text = get_text(
        "order_success",
        lang,
        order_id=order.order_id,
        total=order.total,
        phone=order.customer_phone,
        currency="€",
    ) + save_note

    await callback.message.edit_text(
        success_text, reply_markup=get_order_complete_keyboard(lang)
    )
    await callback.answer(get_text("order_placed", lang))


@router.callback_query(OrderCallback.filter(F.action == "cancel"))
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    """Cancel order and return to cart"""
    lang = await get_user_lang(state)
    cart = await CartService.get_cart(state, callback.from_user.id)

    # Clear order state but keep cart and language
    cart_data = (await state.get_data()).get("cart")
    await state.clear()
    await state.update_data(lang=lang)
    if cart_data:
        await state.update_data(cart=cart_data)

    from app.handlers.cart import format_cart_text

    await callback.message.edit_text(
        format_cart_text(cart, lang),
        reply_markup=get_cart_keyboard(cart, lang),
    )
    await callback.answer(get_text("order_cancelled", lang))
