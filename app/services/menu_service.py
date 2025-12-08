import json
from pathlib import Path
from typing import Optional

from app.models.menu import Menu, Category, MenuItem


class MenuService:
    """Service for menu operations"""

    def __init__(self, menu_file_path: str):
        self.menu_file_path = menu_file_path
        self._menu: Optional[Menu] = None

    def load_menu(self) -> Menu:
        """Load menu from JSON file"""
        if self._menu is None:
            path = Path(self.menu_file_path)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._menu = Menu(**data)
        return self._menu

    def get_menu(self) -> Menu:
        """Get loaded menu"""
        return self.load_menu()

    def get_categories(self) -> list[Category]:
        """Get all categories sorted"""
        menu = self.get_menu()
        return menu.get_sorted_categories()

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        menu = self.get_menu()
        return menu.get_category_by_id(category_id)

    def get_item(self, item_id: str) -> Optional[MenuItem]:
        """Get item by ID"""
        menu = self.get_menu()
        return menu.get_item_by_id(item_id)

    def get_category_for_item(self, item_id: str) -> Optional[Category]:
        """Find which category contains the item"""
        menu = self.get_menu()
        for category in menu.categories:
            for item in category.items:
                if item.id == item_id:
                    return category
        return None

    def reload_menu(self) -> Menu:
        """Force reload menu from file"""
        self._menu = None
        return self.load_menu()
