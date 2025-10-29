# handlers/vocabulary_handler.py - TO'LIQ XATOSIZ KOD
"""
Vocabulary module handler
Handles all vocabulary-related features:
- Add new words (AI-generated)
- Review words (spaced repetition)
- Flashcards system
- Word list viewing
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.operations import (
    get_user, add_vocabulary, get_words_for_review,
    mark_word_learned, get_user_vocabulary, add_xp
)
from database.models import Session, Vocabulary
from keyboards import (
    get_vocabulary_keyboard,
    get_flashcard_keyboard,
    get_back_keyboard
)
from constants import TRANSLATIONS
from services.ai_service import generate_vocabulary_free
from states import BotStates
from config import Config
import logging

logger = logging.getLogger(__name__)

# Create router
vocabulary_router = Router()


# ==================== VOCABULARY MENU ====================
@vocabulary_router.callback_query(F.data == "vocabulary")
async def show_vocabulary_menu(callback: CallbackQuery, state: FSMContext):
    """
    Show vocabulary main menu
    User can choose: Add words, Review, My words, Flashcards
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    text = f"📖 <b>{t['vocabulary']}</b>\n\nChoose an option:"

    await callback.message.edit_text(
        text,
        reply_markup=get_vocabulary_keyboard(user.language),
        parse_mode="HTML"
    )
    await state.set_state(BotStates.vocabulary_menu)
    await callback.answer()

    logger.info(f"User {callback.from_user.id} opened vocabulary menu")


# ==================== ADD NEW WORDS ====================
@vocabulary_router.callback_query(F.data == "vocab_add")
async def add_vocabulary_words(callback: CallbackQuery):
    """
    Generate and add new vocabulary words using AI
    Words are generated based on user's level (A1-C2)
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    await callback.answer("Generating words...")

    try:
        # Generate words using AI
        # use the free generator provided by services.ai_service
        words = await generate_vocabulary_free(user.level, count=Config.WORDS_PER_LESSON)

        if not words or len(words) == 0:
            await callback.message.edit_text(
                "❌ Error generating words. Please try again.",
                reply_markup=get_vocabulary_keyboard(user.language)
            )
            return

        # Add each word to database
        added_count = 0
        for word_data in words:
            try:
                word = word_data.get("word", "")
                translation = word_data.get("translation", "")
                example = word_data.get("example", "")

                # Skip if word or translation is empty
                if not word or not translation:
                    continue

                add_vocabulary(
                    user.telegram_id,
                    word,
                    translation,
                    example,
                    user.level
                )
                added_count += 1

            except Exception as e:
                logger.error(f"Error adding word: {e}")
                continue

        # Award XP
        if added_count > 0:
            add_xp(user.telegram_id, Config.XP_REWARDS["vocabulary_add"])

        # Build response text
        text = f"✅ <b>Added {added_count} new words!</b>\n\n"

        for w in words[:added_count]:
            word = w.get('word', 'N/A')
            translation = w.get('translation', 'N/A')
            example = w.get('example', '')

            text += f"<b>{word}</b> - {translation}\n"
            if example:
                text += f"<i>{example}</i>\n"
            text += "\n"

        text += f"✨ +{Config.XP_REWARDS['vocabulary_add']} XP earned!"

        await callback.message.edit_text(
            text,
            reply_markup=get_vocabulary_keyboard(user.language),
            parse_mode="HTML"
        )

        logger.info(f"User {callback.from_user.id} added {added_count} words")

    except Exception as e:
        logger.error(f"Error in add_vocabulary_words: {e}")
        await callback.message.edit_text(
            "❌ Error generating words. Please try again.",
            reply_markup=get_vocabulary_keyboard(user.language)
        )


# ==================== REVIEW WORDS ====================
@vocabulary_router.callback_query(F.data == "vocab_review")
async def review_vocabulary(callback: CallbackQuery):
    """
    Review words that are due for practice
    Uses spaced repetition algorithm
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    # Get words due for review
    words = get_words_for_review(user.telegram_id, limit=5)

    if not words or len(words) == 0:
        await callback.answer("✅ No words to review right now! Come back later.")
        return

    # Build review text
    text = f"🔄 <b>{t['review_words']}</b>\n\n"
    text += f"<i>Review these {len(words)} words:</i>\n\n"

    for word in words:
        text += f"<b>{word.word}</b> - {word.translation}\n"
        if word.example:
            text += f"<i>{word.example}</i>\n"
        text += f"Reviews: {word.review_count}\n"
        text += "\n"

    # Award XP for reviewing
    add_xp(user.telegram_id, Config.XP_REWARDS["vocabulary_review"])
    text += f"✨ +{Config.XP_REWARDS['vocabulary_review']} XP earned!"

    await callback.message.edit_text(
        text,
        reply_markup=get_vocabulary_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()

    logger.info(f"User {callback.from_user.id} reviewed {len(words)} words")


# ==================== MY WORDS LIST ====================
@vocabulary_router.callback_query(F.data == "vocab_list")
async def show_word_list(callback: CallbackQuery):
    """
    Show user's vocabulary list
    Displays last 10 words with learned status
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    # Get user's vocabulary
    words = get_user_vocabulary(user.telegram_id, limit=10)

    text = f"📝 <b>{t['my_words']} (Last 10)</b>\n\n"

    if words and len(words) > 0:
        for word in words:
            # Status emoji
            status = "✅" if word.learned else "📖"

            text += f"{status} <b>{word.word}</b> - {word.translation}\n"
            text += f"   Level: {word.level} | Reviews: {word.review_count}\n"
            text += "\n"

        # Count statistics
        session = Session()
        total_words = session.query(Vocabulary).filter_by(user_id=user.telegram_id).count()
        learned_words = session.query(Vocabulary).filter_by(user_id=user.telegram_id, learned=True).count()
        session.close()

        text += f"\n📊 <b>Statistics:</b>\n"
        text += f"Total words: {total_words}\n"
        text += f"Learned: {learned_words} ({learned_words * 100 // total_words if total_words > 0 else 0}%)\n"
    else:
        text += "❌ No words yet!\n\n"
        text += f"Use '{t['add_words']}' to start learning."

    await callback.message.edit_text(
        text,
        reply_markup=get_vocabulary_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()

    logger.info(f"User {callback.from_user.id} viewed word list")


# ==================== FLASHCARDS START ====================
@vocabulary_router.callback_query(F.data == "flashcards")
async def start_flashcards(callback: CallbackQuery, state: FSMContext):
    """
    Start flashcard review session
    Shows one word at a time for memorization
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]

    # Get one word for flashcard
    words = get_words_for_review(user.telegram_id, limit=1)

    if not words or len(words) == 0:
        await callback.answer("❌ No flashcards available! Add some words first.")
        return

    word = words[0]

    # Save flashcard state
    await state.update_data(
        current_flashcard=word.id,
        flashcard_side="front"
    )

    # Show front side (Russian word)
    text = f"🗂️ <b>{t['flashcards']}</b>\n\n"
    text += f"<code>{word.word}</code>\n\n"
    text += f"<i>What does this mean?</i>"

    await callback.message.edit_text(
        text,
        reply_markup=get_flashcard_keyboard(user.language),
        parse_mode="HTML"
    )
    await state.set_state(BotStates.flashcard_review)
    await callback.answer()

    logger.info(f"User {callback.from_user.id} started flashcard: {word.word}")


# ==================== FLIP FLASHCARD ====================
@vocabulary_router.callback_query(F.data == "flashcard_flip", StateFilter(BotStates.flashcard_review))
async def flip_flashcard(callback: CallbackQuery, state: FSMContext):
    """
    Flip flashcard to show answer
    Toggles between front (word) and back (translation + example)
    """
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user.language]
    data = await state.get_data()

    vocab_id = data.get("current_flashcard")
    side = data.get("flashcard_side", "front")

    # Get word from database
    session = Session()
    try:
        word = session.query(Vocabulary).filter_by(id=vocab_id).first()

        if not word:
            await callback.answer("❌ Error! Word not found.")
            await state.clear()
            return

        # Toggle side
        if side == "front":
            # Show back (translation + example)
            text = f"🗂️ <b>{t['flashcards']}</b>\n\n"
            text += f"<b>{word.translation}</b>\n\n"
            if word.example:
                text += f"<i>Example:</i>\n{word.example}\n\n"
            text += f"<i>Original word:</i> <code>{word.word}</code>"

            await state.update_data(flashcard_side="back")
        else:
            # Show front (word)
            text = f"🗂️ <b>{t['flashcards']}</b>\n\n"
            text += f"<code>{word.word}</code>\n\n"
            text += f"<i>What does this mean?</i>"

            await state.update_data(flashcard_side="front")

        await callback.message.edit_text(
            text,
            reply_markup=get_flashcard_keyboard(user.language),
            parse_mode="HTML"
        )
        await callback.answer()

    finally:
        session.close()


# ==================== FLASHCARD KNOW IT ====================
@vocabulary_router.callback_query(F.data == "flashcard_know", StateFilter(BotStates.flashcard_review))
async def flashcard_know(callback: CallbackQuery, state: FSMContext):
    """
    User knows the word - mark as learned
    Awards XP and schedules next review
    """
    data = await state.get_data()
    vocab_id = data.get("current_flashcard")

    # Mark word as learned (updates spaced repetition)
    mark_word_learned(vocab_id)

    # Award XP
    xp = Config.XP_REWARDS["flashcard_correct"]
    add_xp(callback.from_user.id, xp)

    await callback.answer(f"✅ Great! +{xp} XP")

    logger.info(f"User {callback.from_user.id} marked word {vocab_id} as known")

    # Load next flashcard
    await start_flashcards(callback, state)


# ==================== FLASHCARD DON'T KNOW ====================
@vocabulary_router.callback_query(F.data == "flashcard_dont", StateFilter(BotStates.flashcard_review))
async def flashcard_dont_know(callback: CallbackQuery, state: FSMContext):
    """
    User doesn't know the word - keep for more practice
    Shows next card without marking as learned
    """
    await callback.answer("💪 Keep practicing!")

    logger.info(f"User {callback.from_user.id} needs more practice")

    # Load next flashcard
    await start_flashcards(callback, state)