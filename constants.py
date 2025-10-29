# constants.py - Constants & Translations
"""
All constants, translations, and achievement definitions
"""

# ==================== TRANSLATIONS ====================
TRANSLATIONS = {
    "uz": {
        "welcome": "🎉 Salom! Russian Learner botiga xush kelibsiz!",
        "choose_language": "🌐 Tilni tanlang:",
        "main_menu": "📚 Asosiy Menyu",
        "profile": "👤 Profil",
        "vocabulary": "📖 Lug'at",
        "grammar": "📝 Grammatika",
        "listening": "🎧 Eshitish",
        "practice": "✍️ Amaliyot",
        "games": "🎮 O'yinlar",
        "settings": "⚙️ Sozlamalar",
        "leaderboard": "🏆 Reyting",
        "achievements": "🎖️ Yutuqlar",
        "flashcards": "🗂️ Flashcards",
        "speaking_duel": "🗣️ Speaking Duel",
        "spy_mission": "🕵️ Spy Mission",
        "word_game": "🎯 So'z o'yini",
        "back": "⬅️ Orqaga",
        "streak": "🔥 Ketma-ketlik",
        "days": "kun",
        "your_rank": "Sizning o'rningiz",
        "review_words": "🔄 So'zlarni takrorlash",
        "add_words": "➕ Yangi so'zlar",
        "my_words": "📝 Mening so'zlarim",
        "start_exercise": "▶️ Mashqni boshlash",
        "notifications": "🔔 Bildirishnomalar",
        "on": "Yoniq",
        "off": "O'chiq",
        "your_level": "Sizning darajangiz",
        "xp_progress": "XP jarayoni",
        "daily_goal": "Kunlik maqsad",
        "flip": "🔄 O'girish",
        "know_it": "✅ Bilaman",
        "dont_know": "❌ Bilmayman",
        "listening_instruction": "Tinglang va eshitganingizni yozing:",
        "practice_instruction": "Rus tilida istalgan narsani yozing:",
        "grammar_instruction": "Javobingizni yozing:",
        "voice_instruction": "Ovozli xabar yuboring yoki yozing:",
    },
    "ru": {
        "welcome": "🎉 Привет! Добро пожаловать в Russian Learner!",
        "choose_language": "🌐 Выберите язык:",
        "main_menu": "📚 Главное меню",
        "profile": "👤 Профиль",
        "vocabulary": "📖 Словарь",
        "grammar": "📝 Грамматика",
        "listening": "🎧 Аудирование",
        "practice": "✍️ Практика",
        "games": "🎮 Игры",
        "settings": "⚙️ Настройки",
        "leaderboard": "🏆 Рейтинг",
        "achievements": "🎖️ Достижения",
        "flashcards": "🗂️ Карточки",
        "speaking_duel": "🗣️ Speaking Duel",
        "spy_mission": "🕵️ Шпионская миссия",
        "word_game": "🎯 Игра в слова",
        "back": "⬅️ Назад",
        "streak": "🔥 Серия",
        "days": "дней",
        "your_rank": "Ваш ранг",
        "review_words": "🔄 Повторить слова",
        "add_words": "➕ Новые слова",
        "my_words": "📝 Мои слова",
        "start_exercise": "▶️ Начать упражнение",
        "notifications": "🔔 Уведомления",
        "on": "Вкл",
        "off": "Выкл",
        "your_level": "Ваш уровень",
        "xp_progress": "XP прогресс",
        "daily_goal": "Дневная цель",
        "flip": "🔄 Перевернуть",
        "know_it": "✅ Знаю",
        "dont_know": "❌ Не знаю",
        "listening_instruction": "Послушайте и напишите, что услышали:",
        "practice_instruction": "Напишите что-нибудь на русском:",
        "grammar_instruction": "Напишите ваш ответ:",
        "voice_instruction": "Отправьте голосовое сообщение или напишите:",
    },
    "en": {
        "welcome": "🎉 Hello! Welcome to Russian Learner!",
        "choose_language": "🌐 Choose Language:",
        "main_menu": "📚 Main Menu",
        "profile": "👤 Profile",
        "vocabulary": "📖 Vocabulary",
        "grammar": "📝 Grammar",
        "listening": "🎧 Listening",
        "practice": "✍️ Practice",
        "games": "🎮 Games",
        "settings": "⚙️ Settings",
        "leaderboard": "🏆 Leaderboard",
        "achievements": "🎖️ Achievements",
        "flashcards": "🗂️ Flashcards",
        "speaking_duel": "🗣️ Speaking Duel",
        "spy_mission": "🕵️ Spy Mission",
        "word_game": "🎯 Word Game",
        "back": "⬅️ Back",
        "streak": "🔥 Streak",
        "days": "days",
        "your_rank": "Your rank",
        "review_words": "🔄 Review Words",
        "add_words": "➕ Add Words",
        "my_words": "📝 My Words",
        "start_exercise": "▶️ Start Exercise",
        "notifications": "🔔 Notifications",
        "on": "On",
        "off": "Off",
        "your_level": "Your level",
        "xp_progress": "XP Progress",
        "daily_goal": "Daily goal",
        "flip": "🔄 Flip",
        "know_it": "✅ Know it",
        "dont_know": "❌ Don't know",
        "listening_instruction": "Listen and write what you hear:",
        "practice_instruction": "Write anything in Russian:",
        "grammar_instruction": "Write your answer:",
        "voice_instruction": "Send a voice message or write:",
    }
}

# ==================== ACHIEVEMENTS ====================
ACHIEVEMENTS = {
    "first_word": {
        "title": "🌟 First Word",
        "desc": "Learn your first word",
        "xp": 10
    },
    "word_master_10": {
        "title": "📚 Word Collector",
        "desc": "Learn 10 words",
        "xp": 50
    },
    "word_master_50": {
        "title": "📖 Vocabulary Expert",
        "desc": "Learn 50 words",
        "xp": 200
    },
    "word_master_100": {
        "title": "🎓 Word Master",
        "desc": "Learn 100 words",
        "xp": 500
    },
    "streak_3": {
        "title": "🔥 On Fire",
        "desc": "3 day streak",
        "xp": 30
    },
    "streak_7": {
        "title": "⚡ Committed",
        "desc": "7 day streak",
        "xp": 100
    },
    "streak_30": {
        "title": "💎 Dedicated",
        "desc": "30 day streak",
        "xp": 500
    },
    "level_a2": {
        "title": "📈 Progress",
        "desc": "Reach A2 level",
        "xp": 100
    },
    "level_b1": {
        "title": "🎯 Intermediate",
        "desc": "Reach B1 level",
        "xp": 300
    },
    "level_b2": {
        "title": "⭐ Advanced",
        "desc": "Reach B2 level",
        "xp": 600
    },
    "duel_win_10": {
        "title": "⚔️ Duelist",
        "desc": "Win 10 duels",
        "xp": 150
    },
    "mission_complete_5": {
        "title": "🕵️ Agent",
        "desc": "Complete 5 missions",
        "xp": 200
    },
}

# ==================== CEFR LEVELS ====================
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

LEVEL_XP_THRESHOLDS = {
    "A1": 0,
    "A2": 2000,
    "B1": 5000,
    "B2": 10000,
    "C1": 18000,
    "C2": 30000
}

# ==================== XP REWARDS ====================
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

# ==================== LEADERBOARD MEDALS ====================
RANK_MEDALS = {
    1: "🥇",
    2: "🥈",
    3: "🥉"
}

# ==================== STREAK EMOJIS ====================
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

# ==================== LEVEL DESCRIPTIONS ====================
LEVEL_DESCRIPTIONS = {
    "A1": "Beginner - Can understand and use familiar everyday expressions",
    "A2": "Elementary - Can communicate in simple routine tasks",
    "B1": "Intermediate - Can deal with most situations while traveling",
    "B2": "Upper Intermediate - Can interact with native speakers fluently",
    "C1": "Advanced - Can use language flexibly for social purposes",
    "C2": "Proficient - Can understand virtually everything heard or read"
}