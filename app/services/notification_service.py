from aiogram import Bot
from loguru import logger

from app.models.order import Order, DeliveryType


class NotificationService:
    """Service for sending order notifications to Telegram channel"""

    def __init__(self, bot: Bot, channel_id: str):
        self.bot = bot
        self.channel_id = channel_id

    def _format_order_for_channel(self, order: Order) -> str:
        """Format order message for kitchen channel"""
        lines = [
            f"🆕 <b>НОВЫЙ ЗАКАЗ #{order.order_id}</b>",
            "",
            f"👤 Клиент: {order.customer_name}",
            f"📞 Телефон: {order.customer_phone}",
        ]

        if order.delivery_type == DeliveryType.DELIVERY:
            lines.append(f"🚗 Доставка: {order.delivery_address}")
        else:
            lines.append("🏪 Самовывоз")

        lines.append(f"🕐 Время: {order.delivery_time}")
        lines.append("")
        lines.append("📋 <b>Заказ:</b>")

        for item in order.items:
            lines.append(f"• {item.name} x{item.quantity} — {item.subtotal}€")

        lines.append("")

        if order.delivery_fee > 0:
            lines.append(f"Подытог: {order.subtotal}€")
            lines.append(f"Доставка: {order.delivery_fee}€")

        lines.append(f"💰 <b>Итого: {order.total}€</b>")

        if order.comment:
            lines.append("")
            lines.append(f"💬 Комментарий: {order.comment}")

        return "\n".join(lines)

    async def send_order_notification(self, order: Order) -> bool:
        """Send order notification to channel"""
        if not self.channel_id:
            logger.warning("Orders channel ID not configured, skipping notification")
            return False

        try:
            message = self._format_order_for_channel(order)

            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="HTML",
            )

            logger.info(f"Order {order.order_id} notification sent to channel")
            return True

        except Exception as e:
            logger.error(f"Failed to send order notification: {e}")
            return False
