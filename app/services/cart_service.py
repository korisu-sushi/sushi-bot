from typing import Optional
from aiogram.fsm.context import FSMContext

from app.models.cart import Cart, CartItem
from app.models.menu import MenuItem


class CartService:
    """Service for cart operations using FSM storage"""

    CART_KEY = "cart"

    @staticmethod
    async def get_cart(state: FSMContext, user_id: int) -> Cart:
        """Get or create cart from state"""
        data = await state.get_data()
        cart_data = data.get(CartService.CART_KEY)

        if cart_data:
            # Reconstruct cart from stored data
            cart = Cart(
                user_id=user_id,
                items={
                    k: CartItem(**v) for k, v in cart_data.get("items", {}).items()
                },
            )
        else:
            cart = Cart(user_id=user_id)

        return cart

    @staticmethod
    async def save_cart(state: FSMContext, cart: Cart) -> None:
        """Save cart to state"""
        cart_data = {
            "user_id": cart.user_id,
            "items": {k: v.model_dump() for k, v in cart.items.items()},
        }
        await state.update_data(**{CartService.CART_KEY: cart_data})

    @staticmethod
    async def add_item(
        state: FSMContext,
        user_id: int,
        item: MenuItem,
        quantity: int = 1,
        lang: str = "en",
    ) -> Cart:
        """Add item to cart"""
        cart = await CartService.get_cart(state, user_id)
        cart.add_item(
            item_id=item.id,
            name=item.get_name(lang),
            price=item.price,
            quantity=quantity,
        )
        await CartService.save_cart(state, cart)
        return cart

    @staticmethod
    async def remove_item(
        state: FSMContext, user_id: int, item_id: str
    ) -> Cart:
        """Remove item from cart"""
        cart = await CartService.get_cart(state, user_id)
        cart.remove_item(item_id)
        await CartService.save_cart(state, cart)
        return cart

    @staticmethod
    async def increment_item(
        state: FSMContext, user_id: int, item_id: str
    ) -> Cart:
        """Increment item quantity"""
        cart = await CartService.get_cart(state, user_id)
        cart.increment_item(item_id)
        await CartService.save_cart(state, cart)
        return cart

    @staticmethod
    async def decrement_item(
        state: FSMContext, user_id: int, item_id: str
    ) -> Cart:
        """Decrement item quantity"""
        cart = await CartService.get_cart(state, user_id)
        cart.decrement_item(item_id)
        await CartService.save_cart(state, cart)
        return cart

    @staticmethod
    async def clear_cart(state: FSMContext, user_id: int) -> Cart:
        """Clear all items from cart"""
        cart = Cart(user_id=user_id)
        await CartService.save_cart(state, cart)
        return cart

    @staticmethod
    async def get_cart_total(state: FSMContext, user_id: int) -> float:
        """Get cart total"""
        cart = await CartService.get_cart(state, user_id)
        return cart.total
