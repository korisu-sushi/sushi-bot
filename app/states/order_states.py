from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    """States for order placement flow"""

    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_delivery_day = State()
    waiting_for_time_slot = State()
    waiting_for_comment = State()
    confirmation = State()
