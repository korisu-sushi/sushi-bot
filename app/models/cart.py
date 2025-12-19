from pydantic import BaseModel
from datetime import datetime


class CartItem(BaseModel):
    """Single item in the cart"""

    item_id: str
    name: str
    price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        """Calculate item subtotal"""
        return self.price * self.quantity


class Cart(BaseModel):
    """Shopping cart for a user"""

    user_id: int
    items: dict[str, CartItem] = {}
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @property
    def total(self) -> float:
        """Calculate cart total"""
        return sum(item.subtotal for item in self.items.values())

    @property
    def item_count(self) -> int:
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.values())

    @property
    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.items) == 0

    def add_item(
        self, item_id: str, name: str, price: float, quantity: int = 1
    ) -> None:
        """Add item to cart or increase quantity"""
        if item_id in self.items:
            self.items[item_id].quantity += quantity
        else:
            self.items[item_id] = CartItem(
                item_id=item_id,
                name=name,
                price=price,
                quantity=quantity,
            )
        self.updated_at = datetime.now()

    def remove_item(self, item_id: str) -> None:
        """Remove item from cart"""
        if item_id in self.items:
            del self.items[item_id]
            self.updated_at = datetime.now()

    def update_quantity(self, item_id: str, quantity: int) -> None:
        """Update item quantity"""
        if item_id in self.items:
            if quantity <= 0:
                self.remove_item(item_id)
            else:
                self.items[item_id].quantity = quantity
                self.updated_at = datetime.now()

    def increment_item(self, item_id: str) -> None:
        """Increase item quantity by 1"""
        if item_id in self.items:
            self.items[item_id].quantity += 1
            self.updated_at = datetime.now()

    def decrement_item(self, item_id: str) -> None:
        """Decrease item quantity by 1, remove if 0"""
        if item_id in self.items:
            self.items[item_id].quantity -= 1
            if self.items[item_id].quantity <= 0:
                self.remove_item(item_id)
            else:
                self.updated_at = datetime.now()

    def clear(self) -> None:
        """Clear all items from cart"""
        self.items = {}
        self.updated_at = datetime.now()

    def get_item(self, item_id: str) -> CartItem | None:
        """Get cart item by ID"""
        return self.items.get(item_id)
