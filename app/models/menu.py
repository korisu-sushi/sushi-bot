from typing import Optional
from pydantic import BaseModel

DEFAULT_LANG = "en"


class LocalizedString(BaseModel):
    """Multilingual string with language variants"""

    en: str
    fr: str = ""
    uk: str = ""
    ru: str = ""

    def get(self, lang: str) -> str:
        """Get text in specified language, fallback to English"""
        value = getattr(self, lang, None)
        if value:
            return value
        return self.en


class MenuItem(BaseModel):
    """Single menu item (roll, sushi, drink, etc.)"""

    id: str
    name: LocalizedString
    description: LocalizedString
    price: int
    weight: str
    pieces: Optional[int] = None
    available: bool = True
    popular: bool = False

    def get_name(self, lang: str = DEFAULT_LANG) -> str:
        """Get item name in specified language"""
        return self.name.get(lang)

    def get_description(self, lang: str = DEFAULT_LANG) -> str:
        """Get item description in specified language"""
        return self.description.get(lang)


class Category(BaseModel):
    """Menu category with items"""

    id: str
    name: LocalizedString
    emoji: str
    sort_order: int
    items: list[MenuItem]

    def get_name(self, lang: str = DEFAULT_LANG) -> str:
        """Get category name in specified language"""
        return self.name.get(lang)

    def get_available_items(self) -> list[MenuItem]:
        """Return only available items"""
        return [item for item in self.items if item.available]


class RestaurantInfo(BaseModel):
    """Restaurant contact info"""

    name: LocalizedString
    phone: str
    working_hours: str
    min_order_amount: int

    def get_name(self, lang: str = DEFAULT_LANG) -> str:
        """Get restaurant name in specified language"""
        return self.name.get(lang)


class Menu(BaseModel):
    """Complete menu structure"""

    version: str
    currency: str
    restaurant: RestaurantInfo
    categories: list[Category]

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """Find category by ID"""
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def get_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        """Find item by ID across all categories"""
        for category in self.categories:
            for item in category.items:
                if item.id == item_id:
                    return item
        return None

    def get_sorted_categories(self) -> list[Category]:
        """Return categories sorted by sort_order"""
        return sorted(self.categories, key=lambda c: c.sort_order)
