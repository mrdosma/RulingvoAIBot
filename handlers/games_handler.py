# handlers/games_handler.py
"""
Games handler - Speaking Duel, Spy Mission, Word Game
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.operations import get_user, add_xp, get_user_vocabulary
from keyboards import get_games_keyboard, get_back_keyboard, get_word_game_keyboard
from services.ai_service import (
    generate_conversation_prompt, generate_conversation_response,
    generate_spy_mission, evaluate_text
)
from states import BotStates
from config import Config
import random
import logging

logger = logging.getLogger(__name__)

games_router = Router()


# ==================== GAMES MENU ====================
@games_router.callback_query(F.data == "games")
async def show_games(callback: CallbackQuery):
    """Show games menu"""
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        "🎮 <b>Games</b>\n\nChoose a game:",
        reply_markup=get_games_keyboard(user.language),
        parse_mode="HTML"
    )
    await callback.answer()


# ==================== SPEAKING DUEL ====================
@games_router.callback_query(F.data == "speaking_duel")
async def start_duel(callback: CallbackQuery, state: FSMContext):
    """Start speaking duel"""
    user = get_user(callback.from_user.id)

    try:
        question = await generate_conversation_prompt(user.level)
        await state.update_data(duel_turn=1)

        text = f"""🗣️ <b>Speaking Duel - Round 1/3</b>

<b>AI:</b> {question}

<i>Reply in Russian:</i>"""

        await callback.message.edit_text(text, parse_mode="HTML")
        await state.set_state(BotStates.speaking_duel)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in start_duel: {e}")
        await callback.answer("Error starting duel")


@games_router.message(StateFilter(BotStates.speaking_duel))
async def handle_duel(message: Message, state: FSMContext):
    """Handle duel response"""
    user = get_user(message.from_user.id)
    data = await state.get_data()
    turn = data.get("duel_turn", 1)

    try:
        evaluation = await evaluate_text(message.text, user.level)

        if turn >= 3:
            # End duel
            score = (evaluation['grammar_score'] + evaluation['vocabulary_score']) / 2
            xp = Config.XP_REWARDS["speaking_duel_win"] if score >= 7 else 30
            add_xp(message.from_user.id, xp)

            result = "🏆 Victory!" if score >= 7 else "💪 Good Try!"

            text = f"""⚔️ <b>Duel Complete!</b>

{result}

<b>Score:</b> {score:.1f}/10
<b>Grammar:</b> {evaluation['grammar_score']}/10
<b>Vocabulary:</b> {evaluation['vocabulary_score']}/10

<b>Feedback:</b>
{evaluation['feedback']}

+{xp} XP!"""

            await message.answer(
                text,
                reply_markup=get_back_keyboard(user.language),
                parse_mode="HTML"
            )
            await state.clear()
        else:
            # Continue duel
            await state.update_data(duel_turn=turn + 1)
            ai_response = await generate_conversation_response(user.level, message.text)

            text = f"""🗣️ <b>Speaking Duel - Round {turn + 1}/3</b>

<b>AI:</b> {ai_response}

<i>Reply in Russian:</i>"""

            await message.answer(text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Error in handle_duel: {e}")
        await message.answer("Error. Please try again.")
        await state.clear()


# ==================== SPY MISSION ====================
@games_router.callback_query(F.data == "spy_mission")
async def start_mission(callback: CallbackQuery, state: FSMContext):
    """Start spy mission"""
    user = get_user(callback.from_user.id)

    try:
        mission = await generate_spy_mission(user.level)

        text = f"""🕵️ <b>Spy Mission</b>

<b>Your Mission:</b>
{mission}

<i>Complete your mission in Russian:</i>"""

        await callback.message.edit_text(text, parse_mode="HTML")
        await state.set_state(BotStates.spy_mission)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in start_mission: {e}")
        await callback.answer("Error starting mission")


@games_router.message(StateFilter(BotStates.spy_mission))
async def complete_mission(message: Message, state: FSMContext):
    """Complete spy mission"""
    user = get_user(message.from_user.id)

    try:
        evaluation = await evaluate_text(message.text, user.level)

        score = (evaluation['grammar_score'] + evaluation['vocabulary_score']) / 2
        xp = Config.XP_REWARDS["spy_mission_complete"] if score >= 7 else 30
        add_xp(message.from_user.id, xp)

        if score >= 8:
            result = "✅ Mission Accomplished!"
            emoji = "🎉"
        elif score >= 6:
            result = "🎯 Mission Complete"
            emoji = "👍"
        else:
            result = "⚠️ Mission Partial"
            emoji = "💪"

        text = f"""{emoji} <b>{result}</b>

<b>Score:</b> {score:.1f}/10

<b>Feedback:</b>
{evaluation['feedback']}

<b>Corrections:</b>
{evaluation.get('corrections', 'Good job!')}

+{xp} XP!"""

        await message.answer(
            text,
            reply_markup=get_back_keyboard(user.language),
            parse_mode="HTML"
        )
        await state.clear()

    except Exception as e:
        logger.error(f"Error in complete_mission: {e}")
        await message.answer("Error evaluating mission.")
        await state.clear()


# ==================== WORD GAME ====================
@games_router.callback_query(F.data == "word_game")
async def start_word_game(callback: CallbackQuery, state: FSMContext):
    """Start word game"""
    user = get_user(callback.from_user.id)
    words = get_user_vocabulary(user.telegram_id, limit=4)

    if len(words) < 4:
        await callback.answer("⚠️ Need at least 4 words! Add vocabulary first.")
        return

    try:
        correct = random.choice(words)
        await state.update_data(word_game_correct=correct.word)

        options = [{"word": w.word, "translation": w.translation} for w in words]

        text = f"""🎯 <b>Word Game</b>

<b>What is the translation of:</b>
<code>{correct.word}</code>

Choose the correct answer:"""

        await callback.message.edit_text(
            text,
            reply_markup=get_word_game_keyboard(options, user.language),
            parse_mode="HTML"
        )
        await state.set_state(BotStates.word_game)
        await callback.answer()

    except Exception as e:
        logger.error(f"Error in start_word_game: {e}")
        await callback.answer("Error starting game")


@games_router.callback_query(F.data.startswith("wordgame_"), StateFilter(BotStates.word_game))
async def check_word_game(callback: CallbackQuery, state: FSMContext):
    """Check word game answer"""
    data = await state.get_data()
    correct = data.get("word_game_correct")
    chosen = callback.data.split("_", 1)[1]

    is_correct = (chosen == correct)
    xp = Config.XP_REWARDS["word_game_correct"] if is_correct else 5
    add_xp(callback.from_user.id, xp)

    if is_correct:
        result = "✅ Correct!"
        emoji = "🎉"
    else:
        result = f"❌ Wrong! Answer: {correct}"
        emoji = "💪"

    await callback.answer(f"{emoji} {result}\n+{xp} XP")

    # Start new round
    await start_word_game(callback, state)