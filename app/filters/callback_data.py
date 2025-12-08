from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix="cat"):
    """Callback for category selection"""

    category_id: str


class ItemCallback(CallbackData, prefix="item"):
    """Callback for item view"""

    item_id: str


class AddToCartCallback(CallbackData, prefix="add"):
    """Callback for adding item to cart"""

    item_id: str
    quantity: int = 1


class CartItemCallback(CallbackData, prefix="cart"):
    """Callback for cart item actions"""

    action: str  # "inc", "dec", "remove"
    item_id: str


class QuantityCallback(CallbackData, prefix="qty"):
    """Callback for quantity adjustment in item view"""

    item_id: str
    action: str  # "inc", "dec"
    current: int


class OrderCallback(CallbackData, prefix="order"):
    """Callback for order actions"""

    action: str  # "confirm", "cancel", "back"
