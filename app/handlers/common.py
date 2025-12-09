from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.keyboards.menu_kb import get_main_menu_keyboard, get_language_keyboard
from app.services.menu_service import MenuService
from app.i18n import get_text, DEFAULT_LANGUAGE

router = Router(name="common")


async def get_user_lang(state: FSMContext) -> str:
    """Get user language from state"""
    data = await state.get_data()
    return data.get("lang", DEFAULT_LANGUAGE)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, menu_service: MenuService):
    """Handle /start command - show language selection"""
    await state.clear()

    # Show language selection first
    await message.answer(
        "🌐 Please choose your language / Choisissez votre langue / "
        "Оберіть мову / Выберите язык:",
        reply_markup=get_language_keyboard(),
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(
    callback: CallbackQuery, state: FSMContext, menu_service: MenuService
):
    """Handle language selection"""
    lang = callback.data.split(":")[1]
    await state.update_data(lang=lang)

    menu = menu_service.get_menu()
    restaurant = menu.restaurant

    welcome_text = get_text(
        "welcome",
        lang,
        name=restaurant.get_name(lang),
        phone=restaurant.phone,
        hours=restaurant.get_working_hours(lang),
    )

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery, state: FSMContext):
    """Show language selection"""
    lang = await get_user_lang(state)
    await callback.message.edit_text(
        get_text("choose_language", lang),
        reply_markup=get_language_keyboard(),
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    """Handle /help command"""
    lang = await get_user_lang(state)
    await message.answer(
        get_text("help_text", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Handle /cancel command - exit any state"""
    lang = await get_user_lang(state)
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            get_text("nothing_to_cancel", lang),
            reply_markup=get_main_menu_keyboard(lang),
        )
        return

    # Keep language when clearing state
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer(
        get_text("action_cancelled", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(
    callback: CallbackQuery, state: FSMContext, menu_service: MenuService
):
    """Return to main menu"""
    lang = await get_user_lang(state)

    # Keep language when clearing state
    await state.clear()
    await state.update_data(lang=lang)

    menu = menu_service.get_menu()
    restaurant = menu.restaurant

    text = get_text("main_menu_text", lang, name=restaurant.get_name(lang))

    await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "show_help")
async def show_help(callback: CallbackQuery, state: FSMContext):
    """Show help"""
    lang = await get_user_lang(state)
    await callback.message.edit_text(
        get_text("help_text", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "show_contacts")
async def show_contacts(
    callback: CallbackQuery, state: FSMContext, menu_service: MenuService
):
    """Show contacts"""
    lang = await get_user_lang(state)
    menu = menu_service.get_menu()
    restaurant = menu.restaurant

    contacts_text = get_text(
        "contacts",
        lang,
        name=restaurant.get_name(lang),
        phone=restaurant.phone,
        hours=restaurant.get_working_hours(lang),
        min_order=restaurant.min_order_amount,
        currency=menu.currency,
    )

    await callback.message.edit_text(
        contacts_text, reply_markup=get_main_menu_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    """Handle noop callbacks (quantity display, etc.)"""
    await callback.answer()
