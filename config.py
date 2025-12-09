from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application configuration using pydantic-settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False

    # Telegram Bot
    bot_token: str = Field(..., validation_alias="BOT_TOKEN")

    # Google Sheets
    google_credentials_path: str = Field(
        "credentials/service_account.json",
        validation_alias="GOOGLE_CREDENTIALS_PATH",
    )
    google_spreadsheet_id: str = Field(
        "", validation_alias="GOOGLE_SPREADSHEET_ID"
    )

    # Menu
    menu_file_path: str = "data/menu.json"

    # Notifications - Telegram channel for orders
    orders_channel_id: str = Field(
        "", validation_alias="ORDERS_CHANNEL_ID"
    )

    # Business settings (in euros)
    min_order_amount: int = 15
    delivery_fee: int = 15
    free_delivery_threshold: int = 75


# Singleton instance
settings = Settings()
