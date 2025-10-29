# database/operations.py - Database Operations
"""
Database CRUD operations
All database queries and updates
"""

from datetime import datetime, timedelta
from typing import List, Optional
import logging

from database.models import (
    Session, User, Vocabulary, Achievement,
    GrammarProgress, Leaderboard, Statistics
)
from config import Config

logger = logging.getLogger(__name__)


# ==================== USER OPERATIONS ====================
def get_user(telegram_id: int) -> User:
    """Get or create user"""
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
        return user
    finally:
        session.close()


def update_user(telegram_id: int, **kwargs):
    """Update user fields"""
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.last_active = datetime.now()
            session.commit()
    finally:
        session.close()


def add_xp(telegram_id: int, amount: int):
    """Add XP to user and handle level up"""
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            user.xp += amount
            user.daily_goal += amount

            # Level up check
            if user.xp >= user.xp_target:
                levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
                current_idx = levels.index(user.level) if user.level in levels else 0
                if current_idx < len(levels) - 1:
                    user.level = levels[current_idx + 1]
                    user.xp = 0
                    user.xp_target = int(user.xp_target * 1.5)
                    check_achievement(telegram_id, f"level_{user.level.lower()}")

            # Update leaderboard
            update_leaderboard(telegram_id, user.xp, user.level, user.username)
            session.commit()

            logger.info(f"User {telegram_id} earned {amount} XP")
    finally:
        session.close()


# ==================== VOCABULARY OPERATIONS ====================
def add_vocabulary(telegram_id: int, word: str, translation: str,
                   example: str, level: str):
    """Add new vocabulary word"""
    session = Session()
    try:
        vocab = Vocabulary(
            user_id=telegram_id,
            word=word,
            translation=translation,
            example=example,
            level=level
        )
        session.add(vocab)
        session.commit()

        # Check word count achievements
        count = session.query(Vocabulary).filter_by(
            user_id=telegram_id, learned=True
        ).count()

        if count == 1:
            check_achievement(telegram_id, "first_word")
        elif count == 10:
            check_achievement(telegram_id, "word_master_10")
        elif count == 50:
            check_achievement(telegram_id, "word_master_50")
        elif count == 100:
            check_achievement(telegram_id, "word_master_100")

    finally:
        session.close()


def get_words_for_review(telegram_id: int, limit: int = 5) -> List[Vocabulary]:
    """Get words due for review"""
    session = Session()
    try:
        words = session.query(Vocabulary).filter(
            Vocabulary.user_id == telegram_id,
            Vocabulary.next_review <= datetime.now()
        ).limit(limit).all()
        return words
    finally:
        session.close()


def mark_word_learned(vocab_id: int):
    """Mark word as learned and schedule next review"""
    session = Session()
    try:
        vocab = session.query(Vocabulary).filter_by(id=vocab_id).first()
        if vocab:
            vocab.learned = True
            vocab.review_count += 1

            # Spaced repetition intervals
            intervals = Config.SPACED_REPETITION_INTERVALS
            next_interval = intervals[
                min(vocab.review_count - 1, len(intervals) - 1)
            ]
            vocab.next_review = datetime.now() + timedelta(days=next_interval)
            session.commit()
    finally:
        session.close()


def get_user_vocabulary(telegram_id: int, limit: int = 10) -> List[Vocabulary]:
    """Get user's vocabulary list"""
    session = Session()
    try:
        words = session.query(Vocabulary).filter_by(
            user_id=telegram_id
        ).order_by(Vocabulary.created_at.desc()).limit(limit).all()
        return words
    finally:
        session.close()


def get_vocabulary_count(telegram_id: int, learned_only: bool = True) -> int:
    """Get count of user's vocabulary"""
    session = Session()
    try:
        query = session.query(Vocabulary).filter_by(user_id=telegram_id)
        if learned_only:
            query = query.filter_by(learned=True)
        return query.count()
    finally:
        session.close()


# ==================== ACHIEVEMENT OPERATIONS ====================
def check_achievement(telegram_id: int, achievement_key: str) -> bool:
    """Check and award achievement"""
    from constants import ACHIEVEMENTS

    session = Session()
    try:
        # Check if already earned
        existing = session.query(Achievement).filter_by(
            user_id=telegram_id,
            achievement_type=achievement_key
        ).first()

        if not existing and achievement_key in ACHIEVEMENTS:
            ach = ACHIEVEMENTS[achievement_key]
            new_achievement = Achievement(
                user_id=telegram_id,
                achievement_type=achievement_key,
                title=ach["title"],
                description=ach["desc"]
            )
            session.add(new_achievement)
            session.commit()

            # Award XP
            add_xp(telegram_id, ach["xp"])

            logger.info(f"Achievement unlocked: {achievement_key} for user {telegram_id}")
            return True

        return False
    finally:
        session.close()


def get_user_achievements(telegram_id: int) -> List[Achievement]:
    """Get all user achievements"""
    session = Session()
    try:
        achievements = session.query(Achievement).filter_by(
            user_id=telegram_id
        ).order_by(Achievement.earned_at.desc()).all()
        return achievements
    finally:
        session.close()


# ==================== LEADERBOARD OPERATIONS ====================
def update_leaderboard(telegram_id: int, total_xp: int, level: str,
                       username: Optional[str] = None):
    """Update leaderboard entry"""
    session = Session()
    try:
        entry = session.query(Leaderboard).filter_by(user_id=telegram_id).first()

        if entry:
            entry.total_xp = total_xp
            entry.level = level
            entry.username = username
            entry.updated_at = datetime.now()
        else:
            entry = Leaderboard(
                user_id=telegram_id,
                total_xp=total_xp,
                level=level,
                username=username
            )
            session.add(entry)

        session.commit()

        # Recalculate ranks
        all_entries = session.query(Leaderboard).order_by(
            Leaderboard.total_xp.desc()
        ).all()

        for idx, e in enumerate(all_entries, 1):
            e.rank = idx

        session.commit()
    finally:
        session.close()


def get_leaderboard(limit: int = 10) -> List[Leaderboard]:
    """Get top users from leaderboard"""
    session = Session()
    try:
        return session.query(Leaderboard).order_by(
            Leaderboard.total_xp.desc()
        ).limit(limit).all()
    finally:
        session.close()


def get_user_rank(telegram_id: int) -> Optional[Leaderboard]:
    """Get user's leaderboard rank"""
    session = Session()
    try:
        return session.query(Leaderboard).filter_by(
            user_id=telegram_id
        ).first()
    finally:
        session.close()


# ==================== STATISTICS OPERATIONS ====================
def add_statistics(telegram_id: int, activity_type: str, score: Optional[float] = None):
    """Add activity statistics"""
    session = Session()
    try:
        stat = Statistics(
            user_id=telegram_id,
            activity_type=activity_type,
            score=score
        )
        session.add(stat)
        session.commit()
    finally:
        session.close()


def get_user_statistics(telegram_id: int, activity_type: Optional[str] = None):
    """Get user statistics"""
    session = Session()
    try:
        query = session.query(Statistics).filter_by(user_id=telegram_id)
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        return query.all()
    finally:
        session.close()


# ==================== STREAK OPERATIONS ====================
def update_streak(telegram_id: int):
    """Update user streak"""
    session = Session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            yesterday = (datetime.now() - timedelta(days=1)).date()

            if user.last_active.date() == yesterday:
                # Continue streak
                user.streak_days += 1

                # Check streak achievements
                if user.streak_days == 3:
                    check_achievement(telegram_id, "streak_3")
                elif user.streak_days == 7:
                    check_achievement(telegram_id, "streak_7")
                elif user.streak_days == 30:
                    check_achievement(telegram_id, "streak_30")

            elif user.last_active.date() < yesterday:
                # Streak broken
                user.streak_days = 0

            # Reset daily goal
            if user.last_active.date() < datetime.now().date():
                user.daily_goal = 0

            user.last_active = datetime.now()
            session.commit()
    finally:
        session.close()


# ==================== GRAMMAR OPERATIONS ====================
def update_grammar_progress(telegram_id: int, topic: str, score: float):
    """Update grammar progress"""
    session = Session()
    try:
        progress = session.query(GrammarProgress).filter_by(
            user_id=telegram_id,
            topic=topic
        ).first()

        if progress:
            # Average score
            progress.score = (progress.score * progress.attempts + score) / (progress.attempts + 1)
            progress.attempts += 1
            progress.last_practiced = datetime.now()
        else:
            progress = GrammarProgress(
                user_id=telegram_id,
                topic=topic,
                score=score,
                attempts=1
            )
            session.add(progress)

        session.commit()
    finally:
        session.close()