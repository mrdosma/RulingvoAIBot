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

# config.py - Configuration Module
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration"""

    # Telegram
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///russian_learner.db")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Redis (for caching)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    USE_REDIS = os.getenv("USE_REDIS", "False").lower() == "true"

    # Bot Settings
    MAX_MESSAGES_PER_MINUTE = int(os.getenv("MAX_MESSAGES_PER_MINUTE", "20"))
    SESSION_TTL = int(os.getenv("SESSION_TTL", "3600"))  # 1 hour

    # Learning Settings
    DAILY_GOAL_XP = int(os.getenv("DAILY_GOAL_XP", "50"))
    WORDS_PER_LESSON = int(os.getenv("WORDS_PER_LESSON", "5"))
    FLASHCARD_REVIEW_LIMIT = int(os.getenv("FLASHCARD_REVIEW_LIMIT", "10"))

    # XP Rewards
    XP_REWARDS = {
        "vocabulary_add": 10,
        "vocabulary_review": 5,
        "flashcard_correct": 5,
        "grammar_exercise": 20,
        "listening_exercise": 30,
        "practice_session": 25,
        "speaking_duel_win": 50,
        "spy_mission_complete": 50,
        "word_game_correct": 15,
        "daily_login": 10,
        "voice_message": 20
    }

    # Spaced Repetition Intervals (in days)
    SPACED_REPETITION_INTERVALS = [1, 3, 7, 14, 30, 60, 90, 180]

    # Notifications
    NOTIFICATION_TIME_HOUR = int(os.getenv("NOTIFICATION_TIME_HOUR", "9"))
    NOTIFICATION_TIME_MINUTE = int(os.getenv("NOTIFICATION_TIME_MINUTE", "0"))

    # File Storage
    TEMP_DIR = os.getenv("TEMP_DIR", "./temp")
    AUDIO_DIR = os.getenv("AUDIO_DIR", "./audio")

    # Sentry (Error Tracking)
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    USE_SENTRY = bool(SENTRY_DSN)

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "bot.log")

    # AI Settings
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "500"))
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_REQUEST_TIMEOUT = int(os.getenv("AI_REQUEST_TIMEOUT", "30"))

    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    MAX_REQUESTS_PER_USER_PER_HOUR = int(os.getenv("MAX_REQUESTS_PER_USER_PER_HOUR", "100"))

    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []

        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")

        if not cls.OPENAI_API_KEY and not cls.GROQ_API_KEY:
            errors.append("Either OPENAI_API_KEY or GROQ_API_KEY is required")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True

    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.AUDIO_DIR, exist_ok=True)


# Validate configuration on import
Config.validate()
Config.create_directories()
