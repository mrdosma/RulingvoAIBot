# handlers/start_handler.py - TO'LIQ KOD
"""
Start command and language selection handler
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.operations import get_user, update_user, update_streak
from keyboards import get_language_keyboard, get_main_menu_keyboard
from constants import TRANSLATIONS
from states import BotStates
import logging

# Use module name for the logger instead of an undefined `name` variable
logger = logging.getLogger(__name__)

start_router = Router()


# ==================== /START COMMAND ====================
@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    try:
        # Get or create user
        user = get_user(message.from_user.id)

        # Update username
        update_user(message.from_user.id, username=message.from_user.username)

        # Update streak
        update_streak(message.from_user.id)

        # Welcome message
        welcome_text = (
            f"{TRANSLATIONS[user.language]['welcome']}\n\n"
            f"{TRANSLATIONS[user.language]['choose_language']}"
        )

        await message.answer(
            welcome_text,
            reply_markup=get_language_keyboard()
        )
        await state.set_state(BotStates.selecting_language)

        logger.info(f"User {message.from_user.id} started the bot")

    except Exception as e:
        logger.error(f"Error in cmd_start: {e}")
        await message.answer(
            "Error starting bot. Please try again with /start"
        )


# ==================== LANGUAGE SELECTION ====================
@start_router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    try:
        lang = callback.data.split("_")[1]

        # Validate language
        if lang not in ["uz", "ru", "en"]:
            await callback.answer("Invalid language!")
            return

        # Update user language
        update_user(callback.from_user.id, language=lang)

        # Show main menu
        await callback.message.edit_text(
            TRANSLATIONS[lang]["main_menu"],
            reply_markup=get_main_menu_keyboard(lang)
        )
        await state.set_state(BotStates.main_menu)
        await callback.answer()

        logger.info(f"User {callback.from_user.id} selected language: {lang}")

    except Exception as e:
        logger.error(f"Error in set_language: {e}")
        await callback.answer("Error setting language. Please try again.")


# ==================== /HELP COMMAND ====================
@start_router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    try:
        user = get_user(message.from_user.id)
        t = TRANSLATIONS[user.language]

        help_text = f"""
🤖 <b>Russian Learner Bot</b>

<b>Available features:</b>

📖 <b>{t['vocabulary']}</b>
- Add new words
- Review with flashcards
- Track learned words

📝 <b>{t['grammar']}</b>
- AI-generated exercises
- Instant feedback
- Progress tracking

🎧 <b>{t['listening']}</b>
- Audio exercises
- Comprehension practice

✍️ <b>{t['practice']}</b>
- Free writing
- AI corrections

🎮 <b>{t['games']}</b>
- Speaking Duel
- Spy Mission
- Word Game

👤 <b>{t['profile']}</b>
- Track your progress
- View statistics
- Check achievements

🏆 <b>{t['leaderboard']}</b>
- Global rankings
- Compete with others

<b>Commands:</b>
/start - Start the bot
/help - Show this help
/menu - Show main menu

<b>Support:</b>
Report issues or suggestions!
        """

        await message.answer(help_text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Error in cmd_help: {e}")
        await message.answer("Error showing help. Please try /start")

# ==================== /MENU COMMAND ====================
@start_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    """Handle /menu command"""
    try:
        user = get_user(message.from_user.id)

        await message.answer(
            TRANSLATIONS[user.language]["main_menu"],
            reply_markup=get_main_menu_keyboard(user.language)
        )
        await state.set_state(BotStates.main_menu)

    except Exception as e:
        logger.error(f"Error in cmd_menu: {e}")
        await message.answer("Error showing menu. Please try /start")

