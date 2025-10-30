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

# utils.py - Utility Functions
import re
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


# ==================== TEXT PROCESSING ====================
def clean_text(text: str) -> str:
    """Clean and normalize text"""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (0-1)"""
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()

    if text1 == text2:
        return 1.0

    # Simple character-based similarity
    max_len = max(len(text1), len(text2))
    if max_len == 0:
        return 0.0

    matches = sum(c1 == c2 for c1, c2 in zip(text1, text2))
    return matches / max_len


def extract_russian_words(text: str) -> List[str]:
    """Extract Russian words from text"""
    pattern = r'[а-яА-ЯёЁ]+'
    return re.findall(pattern, text)


def is_russian_text(text: str) -> bool:
    """Check if text contains Russian characters"""
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    total_chars = len(re.findall(r'[а-яА-ЯёЁa-zA-Z]', text))
    return russian_chars > total_chars * 0.3 if total_chars > 0 else False


# ==================== TIME & DATE ====================
def format_datetime(dt: datetime, lang: str = "en") -> str:
    """Format datetime for display"""
    formats = {
        "en": "%B %d, %Y at %H:%M",
        "ru": "%d %B %Y в %H:%M",
        "uz": "%d %B %Y, %H:%M"
    }
    return dt.strftime(formats.get(lang, formats["en"]))


def time_ago(dt: datetime, lang: str = "en") -> str:
    """Get human-readable time difference"""
    now = datetime.now()
    diff = now - dt

    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"


def get_streak_emoji(days: int) -> str:
    """Get emoji based on streak days"""
    if days == 0:
        return "🔵"
    elif days < 3:
        return "🔥"
    elif days < 7:
        return "🔥🔥"
    elif days < 30:
        return "🔥🔥🔥"
    else:
        return "💎🔥💎"


# ==================== XP & LEVELS ====================
def calculate_level_from_xp(total_xp: int) -> tuple:
    """Calculate level and progress from total XP"""
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    thresholds = [0, 2000, 5000, 10000, 18000, 30000, 50000]

    for i in range(len(thresholds) - 1):
        if total_xp < thresholds[i + 1]:
            level = levels[i]
            xp_in_level = total_xp - thresholds[i]
            xp_needed = thresholds[i + 1] - thresholds[i]
            return level, xp_in_level, xp_needed

    # Max level
    return "C2", total_xp - thresholds[-1], 999999


def get_progress_bar(current: int, target: int, length: int = 10, filled: str = "■", empty: str = "□") -> str:
    """Generate visual progress bar"""
    if target == 0:
        return empty * length

    filled_count = int((current / target) * length)
    filled_count = min(filled_count, length)

    return filled * filled_count + empty * (length - filled_count)


def format_xp(xp: int) -> str:
    """Format XP number with K/M suffixes"""
    if xp >= 1_000_000:
        return f"{xp / 1_000_000:.1f}M"
    elif xp >= 1_000:
        return f"{xp / 1_000:.1f}K"
    else:
        return str(xp)


# ==================== CACHING ====================
def generate_cache_key(prefix: str, *args) -> str:
    """Generate cache key from arguments"""
    key_parts = [prefix] + [str(arg) for arg in args]
    key = ":".join(key_parts)
    return hashlib.md5(key.encode()).hexdigest()


# ==================== VALIDATION ====================
def validate_russian_word(word: str) -> bool:
    """Validate if string is a valid Russian word"""
    if not word or len(word) < 2:
        return False

    if not re.match(r'^[а-яА-ЯёЁ\-]+$', word):
        return False

    return True


def validate_translation(translation: str) -> bool:
    """Validate translation text"""
    if not translation or len(translation) < 1:
        return False

    return True


# ==================== FILE HANDLING ====================
def get_safe_filename(filename: str) -> str:
    """Make filename safe for filesystem"""
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    filename = re.sub(r'[\s]+', '_', filename)
    return filename.lower()


def get_file_size_mb(filepath: str) -> float:
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0


# ==================== STATISTICS ====================
def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return (correct / total) * 100


def get_rank_emoji(rank: int) -> str:
    """Get emoji for leaderboard rank"""
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    elif rank <= 10:
        return "🏅"
    else:
        return "📍"


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


# ==================== WORD PROCESSING ====================
def get_word_difficulty(word: str) -> str:
    """Estimate word difficulty based on length and complexity"""
    length = len(word)

    if length <= 4:
        return "A1"
    elif length <= 6:
        return "A2"
    elif length <= 8:
        return "B1"
    elif length <= 10:
        return "B2"
    else:
        return "C1"


def transliterate_russian(text: str) -> str:
    """Simple Russian to Latin transliteration"""
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    result = []
    for char in text.lower():
        result.append(translit_map.get(char, char))

    return ''.join(result)


# ==================== ERROR HANDLING ====================
def get_error_message(error: Exception, lang: str = "en") -> str:
    """Get user-friendly error message"""
    messages = {
        "en": "Something went wrong. Please try again later.",
        "ru": "Что-то пошло не так. Попробуйте позже.",
        "uz": "Xatolik yuz berdi. Keyinroq urinib ko'ring."
    }

    logger.error(f"Error: {error}")
    return messages.get(lang, messages["en"])


# ==================== ACHIEVEMENT CHECKING ====================
def check_milestone(count: int, milestones: List[int]) -> Optional[int]:
    """Check if count reached a milestone"""
    for milestone in sorted(milestones, reverse=True):
        if count >= milestone:
            return milestone
    return None


# ==================== TEXT FORMATTING ====================
def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


# ==================== ANALYTICS ====================
class PerformanceMetrics:
    """Track performance metrics"""

    def __init__(self):
        self.start_time = datetime.now()
        self.requests = 0
        self.errors = 0
        self.total_response_time = 0.0

    def record_request(self, response_time: float, error: bool = False):
        self.requests += 1
        self.total_response_time += response_time
        if error:
            self.errors += 1

    def get_stats(self) -> dict:
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_response = self.total_response_time / self.requests if self.requests > 0 else 0

        return {
            "uptime": uptime,
            "requests": self.requests,
            "errors": self.errors,
            "error_rate": (self.errors / self.requests * 100) if self.requests > 0 else 0,
            "avg_response_time": avg_response
        }


# ==================== LANGUAGE DETECTION ====================
def detect_language(text: str) -> str:
    """Simple language detection"""
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    latin_chars = len(re.findall(r'[a-zA-Z]', text))

    if russian_chars > latin_chars:
        return "ru"
    else:
        return "en"


# ==================== QUIZ GENERATION ====================
def generate_quiz_options(correct: str, distractors: List[str], count: int = 4) -> List[str]:
    """Generate quiz options with correct answer and distractors"""
    import random

    options = [correct]
    available_distractors = [d for d in distractors if d != correct]

    while len(options) < count and available_distractors:
        distractor = random.choice(available_distractors)
        available_distractors.remove(distractor)
        options.append(distractor)

    random.shuffle(options)
    return options


# ==================== USER FEEDBACK ====================
def generate_encouraging_message(score: float, lang: str = "en") -> str:
    """Generate encouraging message based on score"""
    messages = {
        "en": {
            "high": ["Excellent! 🌟", "Perfect! 💯", "Outstanding! 🎉"],
            "medium": ["Good job! 👍", "Well done! ✨", "Keep it up! 💪"],
            "low": ["Keep practicing! 📚", "You're improving! 🌱", "Don't give up! 💪"]
        },
        "ru": {
            "high": ["Отлично! 🌟", "Превосходно! 💯", "Великолепно! 🎉"],
            "medium": ["Хорошо! 👍", "Молодец! ✨", "Продолжай! 💪"],
            "low": ["Практикуйся! 📚", "Ты прогрессируешь! 🌱", "Не сдавайся! 💪"]
        },
        "uz": {
            "high": ["A'lo! 🌟", "Mukammal! 💯", "Zo'r! 🎉"],
            "medium": ["Yaxshi! 👍", "Ajoyib! ✨", "Davom et! 💪"],
            "low": ["Mashq qil! 📚", "Oldinga! 🌱", "Taslim bo'lma! 💪"]
        }
    }

    import random

    if score >= 8:
        category = "high"
    elif score >= 5:
        category = "medium"
    else:
        category = "low"

    lang_messages = messages.get(lang, messages["en"])
    return random.choice(lang_messages[category])