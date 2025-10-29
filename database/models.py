# database/models.py - Database Models
"""
Database models for Russian Learner Bot
Contains all SQLAlchemy models
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URL, echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ==================== USER MODEL ====================
class User(Base):
    """User profile and progress"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    language = Column(String, default='en')
    level = Column(String, default='A1')
    xp = Column(Integer, default=0)
    xp_target = Column(Integer, default=2000)
    daily_goal = Column(Integer, default=0)
    daily_goal_target = Column(Integer, default=50)
    streak_days = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    notifications_enabled = Column(Boolean, default=True)
    total_time_minutes = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, level={self.level}, xp={self.xp})>"


# ==================== VOCABULARY MODEL ====================
class Vocabulary(Base):
    """User vocabulary with spaced repetition"""
    __tablename__ = 'vocabulary'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    example = Column(Text, nullable=True)
    level = Column(String, nullable=False)
    learned = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    next_review = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Vocabulary(word={self.word}, learned={self.learned})>"


# ==================== ACHIEVEMENT MODEL ====================
class Achievement(Base):
    """User achievements"""
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    achievement_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    earned_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Achievement(type={self.achievement_type}, user={self.user_id})>"


# ==================== GRAMMAR PROGRESS MODEL ====================
class GrammarProgress(Base):
    """Grammar topic progress"""
    __tablename__ = 'grammar_progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    topic = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    last_practiced = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<GrammarProgress(topic={self.topic}, score={self.score})>"


# ==================== LEADERBOARD MODEL ====================
class Leaderboard(Base):
    """Global leaderboard"""
    __tablename__ = 'leaderboard'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    total_xp = Column(Integer, default=0)
    level = Column(String, default='A1')
    rank = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Leaderboard(user={self.user_id}, rank={self.rank}, xp={self.total_xp})>"


# ==================== STATISTICS MODEL ====================
class Statistics(Base):
    """User statistics"""
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    activity_type = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    completed_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Statistics(user={self.user_id}, type={self.activity_type})>"


# ==================== INITIALIZATION ====================
def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(engine)


def drop_all():
    """Drop all tables - USE WITH CAUTION!"""
    Base.metadata.drop_all(engine)


def get_session():
    """Get database session"""
    return Session()