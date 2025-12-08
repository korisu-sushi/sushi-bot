from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderStatus(str, Enum):
    """Order status enum"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DeliveryType(str, Enum):
    """Delivery type enum"""

    DELIVERY = "delivery"
    PICKUP = "pickup"


class OrderItem(BaseModel):
    """Single item in order"""

    item_id: str
    name: str
    price: int
    quantity: int
    subtotal: int


class Order(BaseModel):
    """Complete order model"""

    order_id: str
    user_id: int
    username: Optional[str] = None

    # Customer info
    customer_name: str
    customer_phone: str

    # Delivery info
    delivery_type: DeliveryType
    delivery_address: Optional[str] = None
    delivery_time: str

    # Order details
    items: list[OrderItem]
    subtotal: int
    delivery_fee: int = 0
    total: int
    comment: Optional[str] = None

    # Status tracking
    status: OrderStatus = OrderStatus.PENDING

    # Timestamps
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_cart(
        cls,
        order_id: str,
        user_id: int,
        username: Optional[str],
        customer_name: str,
        customer_phone: str,
        delivery_type: DeliveryType,
        delivery_address: Optional[str],
        delivery_time: str,
        cart_items: dict,
        delivery_fee: int = 0,
        comment: Optional[str] = None,
    ) -> "Order":
        """Create order from cart items"""
        items = []
        subtotal = 0

        for item_id, cart_item in cart_items.items():
            item_subtotal = cart_item.price * cart_item.quantity
            items.append(
                OrderItem(
                    item_id=item_id,
                    name=cart_item.name,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    subtotal=item_subtotal,
                )
            )
            subtotal += item_subtotal

        now = datetime.now()

        return cls(
            order_id=order_id,
            user_id=user_id,
            username=username,
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_type=delivery_type,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            items=items,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=subtotal + delivery_fee,
            comment=comment,
            status=OrderStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
