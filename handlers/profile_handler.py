# handlers/profile_handler.py - Profile & Statistics
"""
Handles profile, leaderboard, and achievements
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.operations import (
    get_user, get_vocabulary_count, get_user_achievements,
    get_leaderboard, get_user_rank
)
from keyboards import get_back_keyboard
from constants import TRANSLATIONS, ACHIEVEMENTS, RANK_MEDALS
from utils import get_progress_bar, get_streak_emoji

profile_router = Router()


# ==================== PROFILE ====================
@profile_router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    """Show user profile"""
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    # Get statistics
    learned_count = get_vocabulary_count(user.telegram_id, learned_only=True)
    achievements_count = len(get_user_achievements(user.telegram_id))

    # Progress bars
    xp_bar = get_progress_bar(user.xp, user.xp_target, length=10)
    goal_bar = get_progress_bar(user.daily_goal, user.daily_goal_target, length=10)
    streak_emoji = get_streak_emoji(user.streak_days)

    profile_text = f"""
👤 <b>Profile</b>

📊 {t['your_level']}: <b>{user.level}</b>
⚡ {t['xp_progress']}:
[{xp_bar}] {user.xp}/{user.xp_target} XP

🎯 {t['daily_goal']}:
[{goal_bar}] {user.daily_goal}/{user.daily_goal_target} XP

{streak_emoji} {t['streak']}: <b>{user.streak_days}</b> {t['days']}

📚 Words Learned: <b>{learned_count}</b>
🏆 Achievements: <b>{achievements_count}/{len(ACHIEVEMENTS)}</b>
⏱️ Total Time: <b>{user.total_time_minutes}</b> min
    """

    await callback.message.edit_text(
        profile_text,
        reply_markup=get_back_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()


# ==================== LEADERBOARD ====================
@profile_router.callback_query(F.data == "leaderboard")
async def show_leaderboard(callback: CallbackQuery):
    """Show global leaderboard"""
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    # Get top users
    top_users = get_leaderboard(limit=10)
    my_rank = get_user_rank(user.telegram_id)

    text = "🏆 <b>Leaderboard</b>\n\n"

    for entry in top_users:
        medal = RANK_MEDALS.get(entry.rank, f"{entry.rank}.")
        name = entry.username or f"User{entry.user_id}"
        text += f"{medal} <b>{name}</b> - {entry.level} ({entry.total_xp} XP)\n"

    if my_rank and my_rank.rank > 10:
        text += f"\n...\n"
        text += f"📍 {t['your_rank']}: <b>#{my_rank.rank}</b> ({my_rank.total_xp} XP)"
    elif my_rank:
        text += f"\n{t['your_rank']}: <b>#{my_rank.rank}</b>"

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()


# ==================== ACHIEVEMENTS ====================
@profile_router.callback_query(F.data == "achievements")
async def show_achievements(callback: CallbackQuery):
    """Show user achievements"""
    user = get_user(callback.from_user.id)

    user_achievements = get_user_achievements(user.telegram_id)
    unlocked_types = {ach.achievement_type for ach in user_achievements}

    text = "🎖️ <b>Achievements</b>\n\n"

    # Show unlocked achievements
    if user_achievements:
        text += "<b>Unlocked:</b>\n"
        for ach in user_achievements:
            text += f"{ach.title}\n<i>{ach.description}</i>\n\n"

    # Show locked achievements
    locked = [key for key in ACHIEVEMENTS.keys() if key not in unlocked_types]
    if locked:
        text += "\n<b>Locked:</b>\n"
        for key in locked[:5]:  # Show first 5 locked
            ach = ACHIEVEMENTS[key]
            text += f"🔒 {ach['title']} - {ach['desc']}\n"

    text += f"\n<b>Progress:</b> {len(user_achievements)}/{len(ACHIEVEMENTS)}"

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()