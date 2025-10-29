# handlers/menu_handler.py - Menu Navigation
"""
Handles main menu navigation
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.operations import get_user
from keyboards import get_main_menu_keyboard
from constants import TRANSLATIONS
from states import BotStates

menu_router = Router()


# ==================== MAIN MENU ====================
@menu_router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery, state: FSMContext):
    """Show main menu"""
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        TRANSLATIONS[user.language]["main_menu"],
        reply_markup=get_main_menu_keyboard(user.language)
    )
    await state.set_state(BotStates.main_menu)
    await callback.answer()