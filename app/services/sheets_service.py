import json
from datetime import datetime
from typing import Optional

from loguru import logger

from app.models.order import Order, OrderStatus

# Google Sheets imports - may not be available
try:
    import gspread_asyncio
    from google.oauth2.service_account import Credentials

    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    logger.warning(
        "Google Sheets libraries not installed. "
        "Orders will not be saved to sheets."
    )


class GoogleSheetsService:
    """Async Google Sheets service for order management"""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    HEADERS = [
        "order_id",
        "created_at",
        "status",
        "user_id",
        "username",
        "customer_name",
        "customer_phone",
        "delivery_type",
        "delivery_address",
        "delivery_time",
        "items",
        "subtotal",
        "delivery_fee",
        "total",
        "comment",
    ]

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self._agcm: Optional["gspread_asyncio.AsyncioGspreadClientManager"] = None
        self._initialized = False

    def _get_credentials(self) -> "Credentials":
        """Create credentials from service account file"""
        return Credentials.from_service_account_file(
            self.credentials_path, scopes=self.SCOPES
        )

    async def _get_client_manager(
        self,
    ) -> "gspread_asyncio.AsyncioGspreadClientManager":
        """Get or create the async client manager"""
        if not SHEETS_AVAILABLE:
            raise RuntimeError("Google Sheets libraries not installed")

        if self._agcm is None:
            self._agcm = gspread_asyncio.AsyncioGspreadClientManager(
                lambda: self._get_credentials()
            )
        return self._agcm

    async def _get_worksheet(self, sheet_name: str = "Orders"):
        """Get worksheet by name"""
        agcm = await self._get_client_manager()
        agc = await agcm.authorize()
        spreadsheet = await agc.open_by_key(self.spreadsheet_id)

        try:
            worksheet = await spreadsheet.worksheet(sheet_name)
        except Exception:
            # Create worksheet if it doesn't exist
            worksheet = await spreadsheet.add_worksheet(
                title=sheet_name, rows=1000, cols=20
            )
            # Add headers
            await worksheet.append_row(self.HEADERS)

        return worksheet

    async def _ensure_headers(self, worksheet) -> None:
        """Ensure headers exist in worksheet"""
        if not self._initialized:
            first_row = await worksheet.row_values(1)
            if not first_row or first_row[0] != "order_id":
                await worksheet.insert_row(self.HEADERS, 1)
            self._initialized = True

    async def save_order(self, order: Order) -> bool:
        """Save order to Google Sheets"""
        if not SHEETS_AVAILABLE:
            logger.warning("Google Sheets not available, order not saved")
            return False

        if not self.spreadsheet_id:
            logger.warning("No spreadsheet ID configured, order not saved")
            return False

        try:
            worksheet = await self._get_worksheet()
            await self._ensure_headers(worksheet)

            # Format items for storage
            items_str = "; ".join(
                f"{item.name} x{item.quantity} ({item.subtotal}€)"
                for item in order.items
            )

            row = [
                order.order_id,
                order.created_at.isoformat(),
                order.status.value,
                str(order.user_id),
                order.username or "",
                order.customer_name,
                order.customer_phone,
                order.delivery_type.value,
                order.delivery_address or "Самовывоз",
                order.delivery_time,
                items_str,
                str(order.subtotal),
                str(order.delivery_fee),
                str(order.total),
                order.comment or "",
            ]

            await worksheet.append_row(row)
            logger.info(f"Order {order.order_id} saved to Google Sheets")
            return True

        except Exception as e:
            logger.error(f"Error saving order to sheets: {e}")
            return False

    async def get_next_order_id(self) -> str:
        """Generate next order ID"""
        today = datetime.now().strftime("%Y%m%d")
        prefix = f"ORD-{today}-"

        if not SHEETS_AVAILABLE or not self.spreadsheet_id:
            # Fallback to timestamp-based ID
            return f"{prefix}{datetime.now().strftime('%H%M%S')}"

        try:
            worksheet = await self._get_worksheet()
            all_values = await worksheet.col_values(1)

            # Find today's orders
            today_orders = [v for v in all_values if v.startswith(prefix)]

            if today_orders:
                numbers = []
                for o in today_orders:
                    try:
                        num = int(o.split("-")[-1])
                        numbers.append(num)
                    except ValueError:
                        continue
                next_num = max(numbers) + 1 if numbers else 1
            else:
                next_num = 1

            return f"{prefix}{next_num:03d}"

        except Exception as e:
            logger.error(f"Error generating order ID: {e}")
            return f"{prefix}{datetime.now().strftime('%H%M%S')}"

    async def update_order_status(
        self,
        order_id: str,
        status: OrderStatus,
    ) -> bool:
        """Update order status (for future admin bot)"""
        if not SHEETS_AVAILABLE or not self.spreadsheet_id:
            return False

        try:
            worksheet = await self._get_worksheet()
            cell = await worksheet.find(order_id)

            if not cell:
                return False

            # Update status (column C = 3)
            await worksheet.update_cell(cell.row, 3, status.value)
            logger.info(f"Order {order_id} status updated to {status.value}")
            return True

        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False
