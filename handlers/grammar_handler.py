# handlers/grammar_handler.py
"""
Grammar exercises handler
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.operations import get_user, add_xp, update_grammar_progress
from keyboards import get_back_keyboard
from services.ai_service import generate_grammar_exercise, evaluate_text
from states import BotStates
from config import Config
import logging

logger = logging.getLogger(__name__)

grammar_router = Router()


@grammar_router.callback_query(F.data == "grammar")
async def start_grammar(callback: CallbackQuery, state: FSMContext):
    """Start grammar exercise"""
    user = get_user(callback.from_user.id)
    await callback.answer("Generating exercise...")

    try:
        exercise = await generate_grammar_exercise(user.level)
        await state.update_data(grammar_answer=exercise.get("answer", ""))

        text = f"""📝 <b>Grammar - {user.level}</b>

<b>Rule:</b> {exercise.get('rule', 'Grammar practice')}

<b>Example:</b> {exercise.get('example', '')}

<b>Question:</b> {exercise.get('question', '')}

<i>Type your answer:</i>"""

        await callback.message.edit_text(
            text,
            reply_markup=get_back_keyboard(user.language),
            parse_mode="HTML"
        )
        await state.set_state(BotStates.grammar_exercise)

    except Exception as e:
        logger.error(f"Error in start_grammar: {e}")
        await callback.message.edit_text(
            "Error generating exercise. Please try again.",
            reply_markup=get_back_keyboard(user.language)
        )


@grammar_router.message(StateFilter(BotStates.grammar_exercise))
async def check_grammar(message: Message, state: FSMContext):
    """Check grammar answer"""
    user = get_user(message.from_user.id)

    try:
        evaluation = await evaluate_text(message.text, user.level)

        score = evaluation.get('grammar_score', 0)
        xp = Config.XP_REWARDS["grammar_exercise"]
        add_xp(message.from_user.id, xp)

        # Update progress
        update_grammar_progress(message.from_user.id, "general", score)

        text = f"""✅ <b>Result:</b>

<b>Grammar:</b> {score}/10
<b>Vocabulary:</b> {evaluation.get('vocabulary_score', 0)}/10

<b>Feedback:</b>
{evaluation.get('feedback', 'Good work!')}

<b>Corrections:</b>
{evaluation.get('corrections', 'None')}

+{xp} XP!"""

        await message.answer(
            text,
            reply_markup=get_back_keyboard(user.language),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in check_grammar: {e}")
        await message.answer("Error checking answer. Please try again.")