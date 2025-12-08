"""
Translations for the Sushi Bot.
Supported languages: en, fr, uk, ru
"""

LANGUAGES = {
    "en": {"flag": "🇬🇧", "name": "English"},
    "fr": {"flag": "🇫🇷", "name": "Français"},
    "uk": {"flag": "🇺🇦", "name": "Українська"},
    "ru": {"flag": "🇷🇺", "name": "Русский"},
}

DEFAULT_LANGUAGE = "en"

TEXTS = {
    # ==================== COMMON ====================
    "choose_language": {
        "en": "🌐 Choose your language:",
        "fr": "🌐 Choisissez votre langue:",
        "uk": "🌐 Оберіть мову:",
        "ru": "🌐 Выберите язык:",
    },
    "welcome": {
        "en": "🍣 <b>Welcome to {name}!</b>\n\nHere you can order fresh sushi and rolls for delivery or pickup.\n\n📞 Phone: {phone}\n🕐 Hours: {hours}\n\nChoose an action from the menu below:",
        "fr": "🍣 <b>Bienvenue chez {name}!</b>\n\nVous pouvez commander des sushis et des rouleaux frais pour la livraison ou à emporter.\n\n📞 Téléphone: {phone}\n🕐 Horaires: {hours}\n\nChoisissez une action dans le menu ci-dessous:",
        "uk": "🍣 <b>Ласкаво просимо до {name}!</b>\n\nТут ви можете замовити свіжі суші та роли з доставкою або самовивозом.\n\n📞 Телефон: {phone}\n🕐 Години роботи: {hours}\n\nОберіть дію з меню нижче:",
        "ru": "🍣 <b>Добро пожаловать в {name}!</b>\n\nЗдесь вы можете заказать свежие суши и роллы с доставкой или самовывозом.\n\n📞 Телефон: {phone}\n🕐 Часы работы: {hours}\n\nВыберите действие из меню ниже:",
    },
    "main_menu_title": {
        "en": "🍣 <b>{name}</b>\n\nChoose an action:",
        "fr": "🍣 <b>{name}</b>\n\nChoisissez une action:",
        "uk": "🍣 <b>{name}</b>\n\nОберіть дію:",
        "ru": "🍣 <b>{name}</b>\n\nВыберите действие:",
    },

    "main_menu_text": {
        "en": "🍣 <b>{name}</b>\n\nChoose an action:",
        "fr": "🍣 <b>{name}</b>\n\nChoisissez une action:",
        "uk": "🍣 <b>{name}</b>\n\nОберіть дію:",
        "ru": "🍣 <b>{name}</b>\n\nВыберите действие:",
    },

    # ==================== BUTTONS ====================
    "btn_menu": {
        "en": "Menu",
        "fr": "Menu",
        "uk": "Меню",
        "ru": "Меню",
    },
    "btn_cart": {
        "en": "Cart",
        "fr": "Panier",
        "uk": "Кошик",
        "ru": "Корзина",
    },
    "btn_contacts": {
        "en": "Contacts",
        "fr": "Contacts",
        "uk": "Контакти",
        "ru": "Контакты",
    },
    "btn_help": {
        "en": "Help",
        "fr": "Aide",
        "uk": "Допомога",
        "ru": "Помощь",
    },
    "btn_language": {
        "en": "Language",
        "fr": "Langue",
        "uk": "Мова",
        "ru": "Язык",
    },
    "btn_back": {
        "en": "◀️ Back",
        "fr": "◀️ Retour",
        "uk": "◀️ Назад",
        "ru": "◀️ Назад",
    },
    "btn_back_to_menu": {
        "en": "◀️ Back to menu",
        "fr": "◀️ Retour au menu",
        "uk": "◀️ Назад до меню",
        "ru": "◀️ Назад в меню",
    },
    "btn_back_categories": {
        "en": "Back to categories",
        "fr": "Retour aux catégories",
        "uk": "Назад до категорій",
        "ru": "Назад к категориям",
    },
    "btn_main_menu": {
        "en": "Main menu",
        "fr": "Menu principal",
        "uk": "Головне меню",
        "ru": "Главное меню",
    },
    "btn_add_to_cart": {
        "en": "Add to cart",
        "fr": "Ajouter au panier",
        "uk": "Додати до кошика",
        "ru": "В корзину",
    },
    "btn_checkout": {
        "en": "Checkout",
        "fr": "Commander",
        "uk": "Оформити замовлення",
        "ru": "Оформить заказ",
    },
    "btn_clear": {
        "en": "Clear",
        "fr": "Vider",
        "uk": "Очистити",
        "ru": "Очистить",
    },
    "btn_continue_shopping": {
        "en": "Continue shopping",
        "fr": "Continuer les achats",
        "uk": "Продовжити покупки",
        "ru": "Продолжить покупки",
    },
    "btn_go_to_menu": {
        "en": "Go to menu",
        "fr": "Aller au menu",
        "uk": "Перейти до меню",
        "ru": "Перейти в меню",
    },
    "btn_delivery": {
        "en": "Delivery",
        "fr": "Livraison",
        "uk": "Доставка",
        "ru": "Доставка",
    },
    "btn_pickup": {
        "en": "Pickup",
        "fr": "À emporter",
        "uk": "Самовивіз",
        "ru": "Самовывоз",
    },
    "btn_asap": {
        "en": "As soon as possible",
        "fr": "Dès que possible",
        "uk": "Якнайшвидше",
        "ru": "Как можно скорее",
    },
    "btn_in_1_hour": {
        "en": "In 1 hour",
        "fr": "Dans 1 heure",
        "uk": "Через 1 годину",
        "ru": "Через 1 час",
    },
    "btn_in_2_hours": {
        "en": "In 2 hours",
        "fr": "Dans 2 heures",
        "uk": "Через 2 години",
        "ru": "Через 2 часа",
    },
    "btn_skip": {
        "en": "Skip",
        "fr": "Passer",
        "uk": "Пропустити",
        "ru": "Пропустить",
    },
    "btn_confirm_order": {
        "en": "Confirm order",
        "fr": "Confirmer la commande",
        "uk": "Підтвердити замовлення",
        "ru": "Подтвердить заказ",
    },
    "btn_cancel": {
        "en": "Cancel",
        "fr": "Annuler",
        "uk": "Скасувати",
        "ru": "Отменить",
    },
    "btn_new_order": {
        "en": "New order",
        "fr": "Nouvelle commande",
        "uk": "Нове замовлення",
        "ru": "Новый заказ",
    },
    "btn_back_to_cart": {
        "en": "Back to cart",
        "fr": "Retour au panier",
        "uk": "Назад до кошика",
        "ru": "Назад в корзину",
    },

    # ==================== MENU ====================
    "menu_title": {
        "en": "📋 <b>Menu</b>\n\nChoose a category:",
        "fr": "📋 <b>Menu</b>\n\nChoisissez une catégorie:",
        "uk": "📋 <b>Меню</b>\n\nОберіть категорію:",
        "ru": "📋 <b>Меню</b>\n\nВыберите категорию:",
    },
    "category_title": {
        "en": "{emoji} <b>{name}</b>\n\nChoose a dish:",
        "fr": "{emoji} <b>{name}</b>\n\nChoisissez un plat:",
        "uk": "{emoji} <b>{name}</b>\n\nОберіть страву:",
        "ru": "{emoji} <b>{name}</b>\n\nВыберите блюдо:",
    },
    "item_weight": {
        "en": "📦 Weight: {weight}",
        "fr": "📦 Poids: {weight}",
        "uk": "📦 Вага: {weight}",
        "ru": "📦 Вес: {weight}",
    },
    "item_pieces": {
        "en": "{pieces} pcs",
        "fr": "{pieces} pcs",
        "uk": "{pieces} шт",
        "ru": "{pieces} шт",
    },
    "item_price": {
        "en": "💰 Price: <b>{price}€</b>",
        "fr": "💰 Prix: <b>{price}€</b>",
        "uk": "💰 Ціна: <b>{price}€</b>",
        "ru": "💰 Цена: <b>{price}€</b>",
    },
    "item_popular": {
        "en": "⭐ Popular dish",
        "fr": "⭐ Plat populaire",
        "uk": "⭐ Популярна страва",
        "ru": "⭐ Популярное блюдо",
    },
    "added_to_cart": {
        "en": "✅ {name} x{quantity} added to cart!",
        "fr": "✅ {name} x{quantity} ajouté au panier!",
        "uk": "✅ {name} x{quantity} додано до кошика!",
        "ru": "✅ {name} x{quantity} добавлено в корзину!",
    },
    "item_detail": {
        "en": "<b>{name}</b>\n{description}\n\n📦 Weight: {weight}{pieces}\n💰 Price: <b>{price}{currency}</b>{popular}",
        "fr": "<b>{name}</b>\n{description}\n\n📦 Poids: {weight}{pieces}\n💰 Prix: <b>{price}{currency}</b>{popular}",
        "uk": "<b>{name}</b>\n{description}\n\n📦 Вага: {weight}{pieces}\n💰 Ціна: <b>{price}{currency}</b>{popular}",
        "ru": "<b>{name}</b>\n{description}\n\n📦 Вес: {weight}{pieces}\n💰 Цена: <b>{price}{currency}</b>{popular}",
    },
    "popular_item": {
        "en": "Popular dish",
        "fr": "Plat populaire",
        "uk": "Популярна страва",
        "ru": "Популярное блюдо",
    },
    "pcs": {
        "en": "pcs",
        "fr": "pcs",
        "uk": "шт",
        "ru": "шт",
    },

    # ==================== CART ====================
    "cart_empty": {
        "en": "🛒 <b>Your cart is empty</b>\n\nAdd dishes from the menu!",
        "fr": "🛒 <b>Votre panier est vide</b>\n\nAjoutez des plats depuis le menu!",
        "uk": "🛒 <b>Ваш кошик порожній</b>\n\nДодайте страви з меню!",
        "ru": "🛒 <b>Корзина пуста</b>\n\nДобавьте блюда из меню!",
    },
    "cart_title": {
        "en": "🛒 <b>Your cart:</b>\n",
        "fr": "🛒 <b>Votre panier:</b>\n",
        "uk": "🛒 <b>Ваш кошик:</b>\n",
        "ru": "🛒 <b>Ваша корзина:</b>\n",
    },
    "total": {
        "en": "Total",
        "fr": "Total",
        "uk": "Разом",
        "ru": "Итого",
    },
    "min_order_warning": {
        "en": "Minimum order: {min_order}{currency}",
        "fr": "Commande minimum: {min_order}{currency}",
        "uk": "Мінімальне замовлення: {min_order}{currency}",
        "ru": "Минимальная сумма заказа: {min_order}{currency}",
    },
    "add_more": {
        "en": "Add {amount}{currency} more",
        "fr": "Ajoutez {amount}{currency} de plus",
        "uk": "Додайте ще {amount}{currency}",
        "ru": "Добавьте ещё на {amount}{currency}",
    },
    "cart_cleared": {
        "en": "🛒 <b>Cart cleared</b>\n\nAdd dishes from the menu!",
        "fr": "🛒 <b>Panier vidé</b>\n\nAjoutez des plats depuis le menu!",
        "uk": "🛒 <b>Кошик очищено</b>\n\nДодайте страви з меню!",
        "ru": "🛒 <b>Корзина очищена</b>\n\nДобавьте блюда из меню!",
    },
    "cart_cleared_notification": {
        "en": "Cart cleared",
        "fr": "Panier vidé",
        "uk": "Кошик очищено",
        "ru": "Корзина очищена",
    },
    "cart_is_empty": {
        "en": "Cart is empty!",
        "fr": "Le panier est vide!",
        "uk": "Кошик порожній!",
        "ru": "Корзина пуста!",
    },
    "min_order_alert": {
        "en": "Minimum order: {amount}{currency}",
        "fr": "Commande minimum: {amount}{currency}",
        "uk": "Мінімальне замовлення: {amount}{currency}",
        "ru": "Минимальная сумма заказа: {amount}{currency}",
    },

    # ==================== ORDER ====================
    "order_title": {
        "en": "📝 <b>Checkout</b>\n\n",
        "fr": "📝 <b>Commander</b>\n\n",
        "uk": "📝 <b>Оформлення замовлення</b>\n\n",
        "ru": "📝 <b>Оформление заказа</b>\n\n",
    },
    "enter_name": {
        "en": "📝 <b>Checkout</b>\n\nEnter your name:",
        "fr": "📝 <b>Commander</b>\n\nEntrez votre nom:",
        "uk": "📝 <b>Оформлення замовлення</b>\n\nВведіть ваше ім'я:",
        "ru": "📝 <b>Оформление заказа</b>\n\nВведите ваше имя:",
    },
    "order_confirmation_title": {
        "en": "📝 <b>Order confirmation</b>\n",
        "fr": "📝 <b>Confirmation de commande</b>\n",
        "uk": "📝 <b>Підтвердження замовлення</b>\n",
        "ru": "📝 <b>Подтверждение заказа</b>\n",
    },
    "name": {
        "en": "Name",
        "fr": "Nom",
        "uk": "Ім'я",
        "ru": "Имя",
    },
    "phone": {
        "en": "Phone",
        "fr": "Téléphone",
        "uk": "Телефон",
        "ru": "Телефон",
    },
    "type": {
        "en": "Type",
        "fr": "Type",
        "uk": "Тип",
        "ru": "Тип",
    },
    "delivery": {
        "en": "Delivery",
        "fr": "Livraison",
        "uk": "Доставка",
        "ru": "Доставка",
    },
    "pickup": {
        "en": "Pickup",
        "fr": "À emporter",
        "uk": "Самовивіз",
        "ru": "Самовывоз",
    },
    "address": {
        "en": "Address",
        "fr": "Adresse",
        "uk": "Адреса",
        "ru": "Адрес",
    },
    "time": {
        "en": "Time",
        "fr": "Heure",
        "uk": "Час",
        "ru": "Время",
    },
    "comment": {
        "en": "Comment",
        "fr": "Commentaire",
        "uk": "Коментар",
        "ru": "Комментарий",
    },
    "order": {
        "en": "Order",
        "fr": "Commande",
        "uk": "Замовлення",
        "ru": "Заказ",
    },
    "subtotal": {
        "en": "Subtotal",
        "fr": "Sous-total",
        "uk": "Підсумок",
        "ru": "Подытог",
    },
    "delivery_fee": {
        "en": "Delivery",
        "fr": "Livraison",
        "uk": "Доставка",
        "ru": "Доставка",
    },
    "delivery_cost": {
        "en": "💰 Delivery fee: {fee}{currency}\n<i>Strasbourg area only</i>",
        "fr": "💰 Frais de livraison: {fee}{currency}\n<i>Zone Strasbourg uniquement</i>",
        "uk": "💰 Вартість доставки: {fee}{currency}\n<i>Тільки район Страсбурга</i>",
        "ru": "💰 Стоимость доставки: {fee}{currency}\n<i>Только район Страсбурга</i>",
    },
    "order_manual_processing": {
        "en": "Order will be processed manually",
        "fr": "La commande sera traitée manuellement",
        "uk": "Замовлення буде оброблено вручну",
        "ru": "Заказ будет обработан вручную",
    },
    "order_placed": {
        "en": "Order placed!",
        "fr": "Commande passée!",
        "uk": "Замовлення прийнято!",
        "ru": "Заказ оформлен!",
    },
    "enter_phone": {
        "en": "📞 Enter your phone number:\n\n<i>Example: +33 6 12 34 56 78 or 06 12 34 56 78</i>",
        "fr": "📞 Entrez votre numéro de téléphone:\n\n<i>Exemple: +33 6 12 34 56 78 ou 06 12 34 56 78</i>",
        "uk": "📞 Введіть номер телефону:\n\n<i>Приклад: +33 6 12 34 56 78 або 06 12 34 56 78</i>",
        "ru": "📞 Введите номер телефона:\n\n<i>Пример: +33 6 12 34 56 78 или 06 12 34 56 78</i>",
    },
    "choose_delivery_type": {
        "en": "🚗 Choose delivery method:\n\n<i>🚚 Delivery: 10€ (Strasbourg only)\n🏪 Pickup: Free</i>",
        "fr": "🚗 Choisissez le mode de livraison:\n\n<i>🚚 Livraison: 10€ (Strasbourg uniquement)\n🏪 À emporter: Gratuit</i>",
        "uk": "🚗 Оберіть спосіб отримання:\n\n<i>🚚 Доставка: 10€ (тільки Страсбург)\n🏪 Самовивіз: Безкоштовно</i>",
        "ru": "🚗 Выберите способ получения:\n\n<i>🚚 Доставка: 10€ (только Страсбург)\n🏪 Самовывоз: Бесплатно</i>",
    },
    "enter_address": {
        "en": "📍 Enter delivery address:\n\n<i>Street, building, apartment</i>",
        "fr": "📍 Entrez l'adresse de livraison:\n\n<i>Rue, bâtiment, appartement</i>",
        "uk": "📍 Введіть адресу доставки:\n\n<i>Вулиця, будинок, квартира</i>",
        "ru": "📍 Введите адрес доставки:\n\n<i>Улица, дом, квартира</i>",
    },
    "choose_time": {
        "en": "🕐 Choose delivery time:",
        "fr": "🕐 Choisissez l'heure de livraison:",
        "uk": "🕐 Оберіть час доставки:",
        "ru": "🕐 Выберите время доставки:",
    },
    "delivery_fee_info": {
        "en": "\n\n💰 Delivery fee: {fee}€\n<i>Strasbourg area only</i>",
        "fr": "\n\n💰 Frais de livraison: {fee}€\n<i>Zone Strasbourg uniquement</i>",
        "uk": "\n\n💰 Вартість доставки: {fee}€\n<i>Тільки район Страсбурга</i>",
        "ru": "\n\n💰 Стоимость доставки: {fee}€\n<i>Только район Страсбурга</i>",
    },
    "enter_comment": {
        "en": "💬 Add a comment to your order:\n\n<i>E.g.: don't ring the doorbell, intercom code, etc.</i>",
        "fr": "💬 Ajoutez un commentaire à votre commande:\n\n<i>Ex.: ne pas sonner, code interphone, etc.</i>",
        "uk": "💬 Додайте коментар до замовлення:\n\n<i>Наприклад: не дзвонити в двері, код домофону тощо</i>",
        "ru": "💬 Добавьте комментарий к заказу:\n\n<i>Например: не звонить в дверь, код домофона и т.д.</i>",
    },
    "order_confirmation": {
        "en": "📝 <b>Order confirmation</b>\n",
        "fr": "📝 <b>Confirmation de commande</b>\n",
        "uk": "📝 <b>Підтвердження замовлення</b>\n",
        "ru": "📝 <b>Подтверждение заказа</b>\n",
    },
    "order_customer": {
        "en": "👤 Name: {name}",
        "fr": "👤 Nom: {name}",
        "uk": "👤 Ім'я: {name}",
        "ru": "👤 Имя: {name}",
    },
    "order_phone": {
        "en": "📞 Phone: {phone}",
        "fr": "📞 Téléphone: {phone}",
        "uk": "📞 Телефон: {phone}",
        "ru": "📞 Телефон: {phone}",
    },
    "order_delivery": {
        "en": "🚗 Delivery: {address}",
        "fr": "🚗 Livraison: {address}",
        "uk": "🚗 Доставка: {address}",
        "ru": "🚗 Доставка: {address}",
    },
    "order_pickup": {
        "en": "🏪 Pickup",
        "fr": "🏪 À emporter",
        "uk": "🏪 Самовивіз",
        "ru": "🏪 Самовывоз",
    },
    "order_time": {
        "en": "🕐 Time: {time}",
        "fr": "🕐 Heure: {time}",
        "uk": "🕐 Час: {time}",
        "ru": "🕐 Время: {time}",
    },
    "order_comment": {
        "en": "💬 Comment: {comment}",
        "fr": "💬 Commentaire: {comment}",
        "uk": "💬 Коментар: {comment}",
        "ru": "💬 Комментарий: {comment}",
    },
    "order_items": {
        "en": "<b>Order:</b>",
        "fr": "<b>Commande:</b>",
        "uk": "<b>Замовлення:</b>",
        "ru": "<b>Заказ:</b>",
    },
    "order_subtotal": {
        "en": "Subtotal: {subtotal}€",
        "fr": "Sous-total: {subtotal}€",
        "uk": "Підсумок: {subtotal}€",
        "ru": "Подытог: {subtotal}€",
    },
    "order_delivery_fee": {
        "en": "Delivery: {fee}€",
        "fr": "Livraison: {fee}€",
        "uk": "Доставка: {fee}€",
        "ru": "Доставка: {fee}€",
    },
    "order_total": {
        "en": "<b>Total: {total}€</b>",
        "fr": "<b>Total: {total}€</b>",
        "uk": "<b>Разом: {total}€</b>",
        "ru": "<b>Итого: {total}€</b>",
    },
    "order_success": {
        "en": "✅ <b>Order #{order_id} confirmed!</b>\n\nTotal: <b>{total}€</b>\n\nWe will contact you at {phone} to confirm the order.\n\nThank you for choosing us! 🍣",
        "fr": "✅ <b>Commande #{order_id} confirmée!</b>\n\nTotal: <b>{total}€</b>\n\nNous vous contacterons au {phone} pour confirmer la commande.\n\nMerci de nous avoir choisis! 🍣",
        "uk": "✅ <b>Замовлення #{order_id} прийнято!</b>\n\nСума: <b>{total}€</b>\n\nМи зв'яжемося з вами за номером {phone} для підтвердження замовлення.\n\nДякуємо, що обрали нас! 🍣",
        "ru": "✅ <b>Заказ #{order_id} принят!</b>\n\nСумма заказа: <b>{total}€</b>\n\nМы свяжемся с вами по номеру {phone} для подтверждения заказа.\n\nСпасибо, что выбрали нас! 🍣",
    },
    "order_manual_note": {
        "en": "\n\n<i>⚠️ Order will be processed manually</i>",
        "fr": "\n\n<i>⚠️ La commande sera traitée manuellement</i>",
        "uk": "\n\n<i>⚠️ Замовлення буде оброблено вручну</i>",
        "ru": "\n\n<i>⚠️ Заказ будет обработан вручную</i>",
    },
    "order_cancelled": {
        "en": "Order cancelled",
        "fr": "Commande annulée",
        "uk": "Замовлення скасовано",
        "ru": "Заказ отменён",
    },
    "order_confirmed_alert": {
        "en": "Order confirmed!",
        "fr": "Commande confirmée!",
        "uk": "Замовлення підтверджено!",
        "ru": "Заказ оформлен!",
    },

    # ==================== DELIVERY TIMES ====================
    "time_asap": {
        "en": "As soon as possible",
        "fr": "Dès que possible",
        "uk": "Якнайшвидше",
        "ru": "Как можно скорее",
    },
    "time_1h": {
        "en": "In 1 hour",
        "fr": "Dans 1 heure",
        "uk": "Через 1 годину",
        "ru": "Через 1 час",
    },
    "time_2h": {
        "en": "In 2 hours",
        "fr": "Dans 2 heures",
        "uk": "Через 2 години",
        "ru": "Через 2 часа",
    },

    # ==================== VALIDATION ====================
    "name_too_short": {
        "en": "Name is too short. Please enter your name:",
        "fr": "Le nom est trop court. Veuillez entrer votre nom:",
        "uk": "Ім'я занадто коротке. Введіть ваше ім'я:",
        "ru": "Имя слишком короткое. Введите ваше имя:",
    },
    "name_too_long": {
        "en": "Name is too long. Please enter your name:",
        "fr": "Le nom est trop long. Veuillez entrer votre nom:",
        "uk": "Ім'я занадто довге. Введіть ваше ім'я:",
        "ru": "Имя слишком длинное. Введите ваше имя:",
    },
    "invalid_phone": {
        "en": "❌ Invalid phone number format.\n\nPlease enter a valid phone number:",
        "fr": "❌ Format de numéro invalide.\n\nVeuillez entrer un numéro valide:",
        "uk": "❌ Невірний формат номера.\n\nВведіть правильний номер телефону:",
        "ru": "❌ Неверный формат номера.\n\nВведите номер телефона:",
    },
    "address_too_short": {
        "en": "Address is too short. Please enter the full address:",
        "fr": "L'adresse est trop courte. Veuillez entrer l'adresse complète:",
        "uk": "Адреса занадто коротка. Введіть повну адресу:",
        "ru": "Адрес слишком короткий. Укажите полный адрес доставки:",
    },
    "comment_too_long": {
        "en": "Comment is too long (max 500 characters). Please try shorter:",
        "fr": "Le commentaire est trop long (max 500 caractères). Essayez plus court:",
        "uk": "Коментар занадто довгий (макс 500 символів). Спробуйте коротше:",
        "ru": "Комментарий слишком длинный (максимум 500 символов). Попробуйте короче:",
    },
    "cart_empty_alert": {
        "en": "Cart is empty!",
        "fr": "Le panier est vide!",
        "uk": "Кошик порожній!",
        "ru": "Корзина пуста!",
    },
    "min_order_alert": {
        "en": "Minimum order: {min}€",
        "fr": "Commande minimum: {min}€",
        "uk": "Мінімальне замовлення: {min}€",
        "ru": "Минимальная сумма заказа: {min}€",
    },

    # ==================== HELP ====================
    "help_text": {
        "en": "📋 <b>How to order:</b>\n\n1. Click «Menu» to browse dishes\n2. Choose a category and add dishes to cart\n3. Go to «Cart» to checkout\n4. Enter delivery details\n5. Confirm your order",
        "fr": "📋 <b>Comment commander:</b>\n\n1. Cliquez sur «Menu» pour voir les plats\n2. Choisissez une catégorie et ajoutez des plats au panier\n3. Allez dans «Panier» pour commander\n4. Entrez les détails de livraison\n5. Confirmez votre commande",
        "uk": "📋 <b>Як зробити замовлення:</b>\n\n1. Натисніть «Меню» для перегляду страв\n2. Оберіть категорію та додайте страви до кошика\n3. Перейдіть до «Кошик» для оформлення\n4. Введіть дані для доставки\n5. Підтвердіть замовлення",
        "ru": "📋 <b>Как сделать заказ:</b>\n\n1. Нажмите «Меню» для просмотра блюд\n2. Выберите категорию и добавьте блюда в корзину\n3. Перейдите в «Корзину» для оформления заказа\n4. Заполните данные для доставки\n5. Подтвердите заказ",
    },

    # ==================== CONTACTS ====================
    "contacts": {
        "en": "📞 <b>Contacts {name}</b>\n\n☎️ Phone: {phone}\n🕐 Hours: {hours}\n\nMinimum order: {min_order}{currency}",
        "fr": "📞 <b>Contacts {name}</b>\n\n☎️ Téléphone: {phone}\n🕐 Horaires: {hours}\n\nCommande minimum: {min_order}{currency}",
        "uk": "📞 <b>Контакти {name}</b>\n\n☎️ Телефон: {phone}\n🕐 Години роботи: {hours}\n\nМінімальне замовлення: {min_order}{currency}",
        "ru": "📞 <b>Контакты {name}</b>\n\n☎️ Телефон: {phone}\n🕐 Время работы: {hours}\n\nМинимальная сумма заказа: {min_order}{currency}",
    },

    # ==================== ERRORS ====================
    "category_not_found": {
        "en": "Category not found",
        "fr": "Catégorie non trouvée",
        "uk": "Категорію не знайдено",
        "ru": "Категория не найдена",
    },
    "item_not_found": {
        "en": "Item not found",
        "fr": "Article non trouvé",
        "uk": "Товар не знайдено",
        "ru": "Товар не найден",
    },
    "action_cancelled": {
        "en": "Action cancelled.",
        "fr": "Action annulée.",
        "uk": "Дію скасовано.",
        "ru": "Действие отменено.",
    },
    "nothing_to_cancel": {
        "en": "Nothing to cancel.",
        "fr": "Rien à annuler.",
        "uk": "Немає чого скасовувати.",
        "ru": "Нечего отменять.",
    },
    "language_changed": {
        "en": "Language changed to English",
        "fr": "Langue changée en Français",
        "uk": "Мову змінено на Українську",
        "ru": "Язык изменён на Русский",
    },
}


def get_text(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Get translated text by key.

    Args:
        key: Translation key
        lang: Language code (en, fr, uk, ru)
        **kwargs: Format arguments

    Returns:
        Translated and formatted string
    """
    if key not in TEXTS:
        return f"[Missing: {key}]"

    translations = TEXTS[key]

    if lang not in translations:
        lang = DEFAULT_LANGUAGE

    text = translations.get(lang, translations.get(DEFAULT_LANGUAGE, f"[Missing: {key}]"))

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text
