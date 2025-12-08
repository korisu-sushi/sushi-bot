import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import settings
from app.handlers import common, menu, cart, order
from app.services.menu_service import MenuService
from app.services.sheets_service import GoogleSheetsService
from app.services.notification_service import NotificationService


async def main():
    """Initialize and start the bot"""

    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        level="DEBUG" if settings.debug else "INFO",
    )

    logger.info(f"Starting bot in {settings.environment} mode")

    # Initialize storage
    storage = MemoryStorage()
    logger.info("Using Memory storage")

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Initialize services
    menu_service = MenuService(settings.menu_file_path)
    sheets_service = GoogleSheetsService(
        credentials_path=settings.google_credentials_path,
        spreadsheet_id=settings.google_spreadsheet_id,
    )
    notification_service = NotificationService(
        bot=bot,
        channel_id=settings.orders_channel_id,
    )

    # Load menu to verify it works
    try:
        menu_data = menu_service.load_menu()
        logger.info(
            f"Menu loaded: {len(menu_data.categories)} categories, "
            f"restaurant: {menu_data.restaurant.name}"
        )
    except Exception as e:
        logger.error(f"Failed to load menu: {e}")
        return

    # Include routers
    dp.include_router(common.router)
    dp.include_router(menu.router)
    dp.include_router(cart.router)
    dp.include_router(order.router)

    # Inject dependencies using middleware approach
    @dp.update.outer_middleware()
    async def inject_dependencies(handler, event, data):
        data["menu_service"] = menu_service
        data["sheets_service"] = sheets_service
        data["notification_service"] = notification_service
        data["settings"] = settings
        return await handler(event, data)

    # Start bot
    logger.info("Bot starting...")

    try:
        # Polling mode for development
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting polling...")

        # Get bot info
        bot_info = await bot.get_me()
        logger.info(f"Bot: @{bot_info.username} ({bot_info.first_name})")

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
