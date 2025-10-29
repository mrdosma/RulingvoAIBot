# handlers/settings_handler.py
"""
Settings handler - language, notifications, reset
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.operations import get_user, update_user
from database.models import Session, Vocabulary, Achievement, GrammarProgress, Leaderboard
from keyboards import (
    get_settings_keyboard, get_language_keyboard,
    get_confirmation_keyboard
)
from constants import TRANSLATIONS
import logging

logger = logging.getLogger(__name__)

settings_router = Router()


# ==================== SETTINGS MENU ====================
@settings_router.callback_query(F.data == "settings")
async def show_settings(callback: CallbackQuery):
    """Show settings menu"""
    user = get_user(callback.from_user.id)

    notif_status = TRANSLATIONS[user.language]["on"] if user.notifications_enabled else TRANSLATIONS[user.language][
        "off"]

    text = f"""⚙️ <b>Settings</b>

<b>Language:</b> {user.language.upper()}
<b>Level:</b> {user.level}
<b>Notifications:</b> {notif_status}

<b>Total XP:</b> {user.xp}
<b>Created:</b> {user.created_at.strftime('%Y-%m-%d')}"""

    await callback.message.edit_text(
        text,
        reply_markup=get_settings_keyboard(user.language, user.notifications_enabled),
        parse_mode="HTML"
    )
    await callback.answer()


# ==================== CHANGE LANGUAGE ====================
@settings_router.callback_query(F.data == "setting_lang")
async def change_language(callback: CallbackQuery):
    """Show language selection"""
    await callback.message.edit_text(
        "🌐 Choose Language / Tilni tanlang:",
        reply_markup=get_language_keyboard()
    )
    await callback.answer()


# ==================== TOGGLE NOTIFICATIONS ====================
@settings_router.callback_query(F.data == "setting_notif")
async def toggle_notifications(callback: CallbackQuery):
    """Toggle notifications"""
    user = get_user(callback.from_user.id)
    new_status = not user.notifications_enabled
    update_user(callback.from_user.id, notifications_enabled=new_status)

    status_text = "enabled ✅" if new_status else "disabled ❌"
    await callback.answer(f"Notifications {status_text}")

    # Refresh settings page
    await show_settings(callback)


# ==================== RESET PROGRESS ====================
@settings_router.callback_query(F.data == "setting_reset")
async def reset_confirm(callback: CallbackQuery):
    """Show reset confirmation"""
    text = """⚠️ <b>DANGER ZONE</b>

This will <b>permanently delete</b>:
- All vocabulary words
- All achievements
- All progress statistics
- Grammar history
- Leaderboard position

<b>This action CANNOT be undone!</b>

Are you absolutely sure?"""

    await callback.message.edit_text(
        text,
        reply_markup=get_confirmation_keyboard("setting_reset_yes", "settings", "en"),
        parse_mode="HTML"
    )
    await callback.answer()


@settings_router.callback_query(F.data == "setting_reset_yes")
async def reset_progress(callback: CallbackQuery):
    """Reset user progress"""
    session = Session()
    try:
        # Delete all user data
        deleted_vocab = session.query(Vocabulary).filter_by(user_id=callback.from_user.id).delete()
        deleted_ach = session.query(Achievement).filter_by(user_id=callback.from_user.id).delete()
        deleted_grammar = session.query(GrammarProgress).filter_by(user_id=callback.from_user.id).delete()
        deleted_leaderboard = session.query(Leaderboard).filter_by(user_id=callback.from_user.id).delete()
        session.commit()

        # Reset user stats
        update_user(
            callback.from_user.id,
            xp=0,
            level="A1",
            xp_target=2000,
            daily_goal=0,
            streak_days=0,
            total_time_minutes=0
        )

        result_text = f"""✅ <b>Progress Reset Complete</b>

<b>Deleted:</b>
- {deleted_vocab} vocabulary words
- {deleted_ach} achievements
- {deleted_grammar} grammar records
- Leaderboard entry

Your account has been reset to A1 level.
Start fresh with /start"""

        await callback.message.edit_text(result_text, parse_mode="HTML")
        await callback.answer("✅ Progress reset successfully!")

        logger.info(f"User {callback.from_user.id} reset their progress")

    except Exception as e:
        logger.error(f"Error resetting progress: {e}")
        await callback.answer("❌ Error resetting progress. Try again.")
    finally:
        session.close()