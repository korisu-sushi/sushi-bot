from datetime import datetime, date, timedelta
import pytz

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.callback_data import OrderCallback, DaySelectionCallback, TimeSlotCallback
from app.i18n import get_text

# Paris timezone for France
PARIS_TZ = pytz.timezone("Europe/Paris")

# Working days (0=Monday, 4=Friday, 6=Sunday)
WORKING_DAYS = [4, 5, 6]  # Fri, Sat, Sun

# Working hours
WORKING_HOUR_START = 13
WORKING_HOUR_END = 19

# Time slots (hourly)
TIME_SLOTS = ["13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]

# Weekday mapping for translations
WEEKDAY_KEYS = [
    "weekday_mon",
    "weekday_tue",
    "weekday_wed",
    "weekday_thu",
    "weekday_fri",
    "weekday_sat",
    "weekday_sun",
]

# Month mapping for translations
MONTH_KEYS = [
    "month_jan",
    "month_feb",
    "month_mar",
    "month_apr",
    "month_may",
    "month_jun",
    "month_jul",
    "month_aug",
    "month_sep",
    "month_oct",
    "month_nov",
    "month_dec",
]


def is_within_working_hours() -> bool:
    """Check if current time is within working hours (Thu-Sun 13:00-19:00)"""
    now = datetime.now(PARIS_TZ)
    if now.weekday() not in WORKING_DAYS:
        return False
    if now.hour < WORKING_HOUR_START or now.hour >= WORKING_HOUR_END:
        return False
    return True


def get_available_days(lang: str = "en", days_ahead: int = 14) -> list[tuple[date, str]]:
    """
    Get available working days for the next N days.

    Returns list of tuples: (date, formatted_label)
    """
    now = datetime.now(PARIS_TZ)
    today = now.date()
    available = []

    for i in range(days_ahead):
        check_date = today + timedelta(days=i)

        # Check if it's a working day
        if check_date.weekday() not in WORKING_DAYS:
            continue

        # If today, check if there are still available slots
        if check_date == today:
            available_slots = get_available_time_slots(check_date)
            if not available_slots:
                continue

        # Format the label
        label = format_date_label(check_date, lang, today)
        available.append((check_date, label))

    return available


def format_date_label(d: date, lang: str, today: date) -> str:
    """Format date for button label"""
    weekday = get_text(WEEKDAY_KEYS[d.weekday()], lang)
    month = get_text(MONTH_KEYS[d.month - 1], lang)

    if d == today:
        today_text = get_text("today", lang)
        return f"{today_text} ({weekday})"
    elif d == today + timedelta(days=1):
        tomorrow_text = get_text("tomorrow", lang)
        return f"{tomorrow_text} ({weekday})"
    else:
        return f"{weekday}, {d.day} {month}"


def get_available_time_slots(selected_date: date) -> list[str]:
    """
    Get available time slots for a given date.
    If it's today, filter out past times.
    """
    now = datetime.now(PARIS_TZ)
    today = now.date()

    if selected_date != today:
        return TIME_SLOTS.copy()

    # Filter out past times for today
    available = []
    for slot in TIME_SLOTS:
        hour = int(slot.split(":")[0])
        # Add 1 hour buffer - if it's 13:30, slot 13:00 is not available
        if hour > now.hour:
            available.append(slot)

    return available


def format_delivery_time(selected_date: date, time_slot: str, lang: str) -> str:
    """Format the final delivery time string for display and storage"""
    today = datetime.now(PARIS_TZ).date()
    weekday = get_text(WEEKDAY_KEYS[selected_date.weekday()], lang)
    month = get_text(MONTH_KEYS[selected_date.month - 1], lang)

    return get_text(
        "delivery_at",
        lang,
        weekday=weekday,
        day=selected_date.day,
        month=month,
        time=time_slot,
    )


def get_day_selection_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Delivery day selection keyboard"""
    builder = InlineKeyboardBuilder()

    available_days = get_available_days(lang)

    # Add day buttons (2 per row)
    for i in range(0, len(available_days), 2):
        row_buttons = []
        for j in range(2):
            if i + j < len(available_days):
                d, label = available_days[i + j]
                row_buttons.append(
                    InlineKeyboardButton(
                        text=label,
                        callback_data=DaySelectionCallback(day=d.isoformat()).pack(),
                    )
                )
        builder.row(*row_buttons)

    # Back button
    builder.row(
        InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data="order_back",
        )
    )

    return builder.as_markup()


def get_time_slot_keyboard(selected_date: date, lang: str = "en") -> InlineKeyboardMarkup:
    """Time slot selection keyboard"""
    builder = InlineKeyboardBuilder()

    available_slots = get_available_time_slots(selected_date)

    # Add time buttons (3 per row)
    for i in range(0, len(available_slots), 3):
        row_buttons = []
        for j in range(3):
            if i + j < len(available_slots):
                slot = available_slots[i + j]
                # Use slot without ":" for callback (e.g., "1300" instead of "13:00")
                slot_callback = slot.replace(":", "")
                row_buttons.append(
                    InlineKeyboardButton(
                        text=slot,
                        callback_data=TimeSlotCallback(time=slot_callback).pack(),
                    )
                )
        builder.row(*row_buttons)

    # Back button
    builder.row(
        InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data="order_back",
        )
    )

    return builder.as_markup()


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
            text=get_text("btn_back", lang),
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
