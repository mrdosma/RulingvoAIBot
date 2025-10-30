# ┌──────────────────────────────────────────────┐
# │ Project : Rulingvo AI System                 │
# │ Author  : Mr.DosMa                           │
# │ Year    : 2025                               │
# │ Langs   : Uzbek / English / Russian          │
# ├──────────────────────────────────────────────┤
# │ Ushbu kod Rulingvo loyihasiga tegishli.     │
# │ This code is property of Rulingvo Project.   │
# │ Этот код принадлежит проекту Rulingvo.      │
# └──────────────────────────────────────────────┘

# scheduler.py - Scheduled Tasks
"""
Background tasks and scheduled notifications
Handles daily reminders and streak updates
"""

import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config
from database.models import Session, User
from database.operations import update_streak
from constants import TRANSLATIONS

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


# ==================== DAILY REMINDERS ====================
async def send_daily_reminders(bot):
    """Send daily learning reminders to users"""
    logger.info("Running daily reminders task...")

    session = Session()
    try:
        # Get users with notifications enabled
        users = session.query(User).filter_by(notifications_enabled=True).all()

        for user in users:
            # Check if user was active today
            if user.last_active.date() < datetime.now().date():
                try:
                    t = TRANSLATIONS[user.language]

                    message = (
                        f"🔔 <b>Daily Reminder!</b>\n\n"
                        f"{t['streak']}: <b>{user.streak_days}</b> {t['days']}\n"
                        f"{t['daily_goal']}: {user.daily_goal}/{user.daily_goal_target} XP\n\n"
                        f"Keep your streak alive! 🔥\n"
                        f"Practice Russian today! 📚"
                    )

                    await bot.send_message(
                        user.telegram_id,
                        message,
                        parse_mode="HTML"
                    )

                    logger.info(f"Reminder sent to user {user.telegram_id}")

                except Exception as e:
                    logger.error(f"Failed to send reminder to {user.telegram_id}: {e}")

        logger.info(f"Daily reminders sent to {len(users)} users")

    finally:
        session.close()


# ==================== STREAK UPDATES ====================
async def update_daily_streaks(bot):
    """Update all user streaks at midnight"""
    logger.info("Running streak update task...")

    session = Session()
    try:
        users = session.query(User).all()

        for user in users:
            update_streak(user.telegram_id)

        session.commit()
        logger.info(f"Streaks updated for {len(users)} users")

    finally:
        session.close()


# ==================== CLEANUP TASKS ====================
async def cleanup_old_files():
    """Clean up old temporary files"""
    logger.info("Running cleanup task...")

    from services.audio_service import cleanup_old_files

    cleanup_old_files(Config.TEMP_DIR, max_age_hours=24)
    cleanup_old_files(Config.AUDIO_DIR, max_age_hours=24)

    logger.info("Cleanup task completed")


# ==================== LEADERBOARD RECALCULATION ====================
async def recalculate_leaderboard():
    """Recalculate leaderboard ranks"""
    logger.info("Running leaderboard recalculation...")

    from database.models import Leaderboard

    session = Session()
    try:
        # Get all entries ordered by XP
        entries = session.query(Leaderboard).order_by(
            Leaderboard.total_xp.desc()
        ).all()

        # Update ranks
        for idx, entry in enumerate(entries, 1):
            entry.rank = idx
            entry.updated_at = datetime.now()

        session.commit()
        logger.info(f"Leaderboard recalculated for {len(entries)} users")

    finally:
        session.close()


# ==================== SETUP SCHEDULER ====================
async def setup_scheduler(bot):
    """Setup all scheduled tasks"""

    # Daily reminders at configured time
    scheduler.add_job(
        send_daily_reminders,
        'cron',
        hour=Config.NOTIFICATION_TIME_HOUR,
        minute=Config.NOTIFICATION_TIME_MINUTE,
        args=[bot]
    )
    logger.info(f"Daily reminders scheduled at {Config.NOTIFICATION_TIME_HOUR}:{Config.NOTIFICATION_TIME_MINUTE:02d}")

    # Streak updates at midnight
    scheduler.add_job(
        update_daily_streaks,
        'cron',
        hour=0,
        minute=1,
        args=[bot]
    )
    logger.info("Streak updates scheduled at 00:01")

    # Cleanup every 6 hours
    scheduler.add_job(
        cleanup_old_files,
        'interval',
        hours=6
    )
    logger.info("Cleanup task scheduled every 6 hours")

    # Leaderboard recalculation every hour
    scheduler.add_job(
        recalculate_leaderboard,
        'interval',
        hours=1
    )
    logger.info("Leaderboard recalculation scheduled every hour")

    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started successfully!")


# ==================== SHUTDOWN ====================
async def shutdown_scheduler():
    """Shutdown scheduler gracefully"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")