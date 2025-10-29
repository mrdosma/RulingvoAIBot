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

# keyboards.py - Keyboard Layouts
"""
All inline keyboard layouts for the bot
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import TRANSLATIONS


# ==================== LANGUAGE SELECTION ====================
def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])


# ==================== MAIN MENU ====================
def get_main_menu_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t["profile"], callback_data="profile"),
            InlineKeyboardButton(text=t["leaderboard"], callback_data="leaderboard")
        ],
        [
            InlineKeyboardButton(text=t["vocabulary"], callback_data="vocabulary"),
            InlineKeyboardButton(text=t["grammar"], callback_data="grammar")
        ],
        [
            InlineKeyboardButton(text=t["listening"], callback_data="listening"),
            InlineKeyboardButton(text=t["practice"], callback_data="practice")
        ],
        [
            InlineKeyboardButton(text=t["games"], callback_data="games"),
            InlineKeyboardButton(text=t["achievements"], callback_data="achievements")
        ],
        [
            InlineKeyboardButton(text=t["settings"], callback_data="settings")
        ]
    ])


# ==================== VOCABULARY MENU ====================
def get_vocabulary_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Vocabulary menu keyboard"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["add_words"], callback_data="vocab_add")],
        [InlineKeyboardButton(text=t["review_words"], callback_data="vocab_review")],
        [InlineKeyboardButton(text=t["my_words"], callback_data="vocab_list")],
        [InlineKeyboardButton(text=t["flashcards"], callback_data="flashcards")],
        [InlineKeyboardButton(text=t["back"], callback_data="main_menu")]
    ])


# ==================== FLASHCARD KEYBOARD ====================
def get_flashcard_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Flashcard review keyboard"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["flip"], callback_data="flashcard_flip")],
        [
            InlineKeyboardButton(text=t["know_it"], callback_data="flashcard_know"),
            InlineKeyboardButton(text=t["dont_know"], callback_data="flashcard_dont")
        ],
        [InlineKeyboardButton(text=t["back"], callback_data="vocabulary")]
    ])


# ==================== GAMES MENU ====================
def get_games_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Games menu keyboard"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["speaking_duel"], callback_data="speaking_duel")],
        [InlineKeyboardButton(text=t["spy_mission"], callback_data="spy_mission")],
        [InlineKeyboardButton(text=t["word_game"], callback_data="word_game")],
        [InlineKeyboardButton(text=t["back"], callback_data="main_menu")]
    ])


# ==================== SETTINGS MENU ====================
def get_settings_keyboard(lang: str = "en", notifications_enabled: bool = True) -> InlineKeyboardMarkup:
    """Settings menu keyboard"""
    t = TRANSLATIONS[lang]
    notif_status = t["on"] if notifications_enabled else t["off"]

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["choose_language"], callback_data="setting_lang")],
        [InlineKeyboardButton(text=f"{t['notifications']}: {notif_status}", callback_data="setting_notif")],
        [InlineKeyboardButton(text="🔄 Reset Progress", callback_data="setting_reset")],
        [InlineKeyboardButton(text=t["back"], callback_data="main_menu")]
    ])


# ==================== BACK BUTTON ====================
def get_back_keyboard(lang: str = "en", callback: str = "main_menu") -> InlineKeyboardMarkup:
    """Simple back button"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["back"], callback_data=callback)]
    ])


# ==================== WORD GAME KEYBOARD ====================
def get_word_game_keyboard(words: list, lang: str = "en") -> InlineKeyboardMarkup:
    """Word game options keyboard"""
    t = TRANSLATIONS[lang]
    buttons = []

    for word in words:
        buttons.append([
            InlineKeyboardButton(
                text=word.get('translation', 'Option'),
                callback_data=f"wordgame_{word.get('word', 'unknown')}"
            )
        ])

    buttons.append([InlineKeyboardButton(text=t["back"], callback_data="games")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==================== LISTENING REPLAY ====================
def get_listening_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Listening exercise keyboard"""
    t = TRANSLATIONS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔊 Play Again", callback_data="listening_replay")],
        [InlineKeyboardButton(text=t["back"], callback_data="main_menu")]
    ])


# ==================== CONFIRMATION KEYBOARD ====================
def get_confirmation_keyboard(confirm_callback: str, cancel_callback: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Confirmation dialog keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yes", callback_data=confirm_callback),
            InlineKeyboardButton(text="❌ No", callback_data=cancel_callback)
        ]
    ])