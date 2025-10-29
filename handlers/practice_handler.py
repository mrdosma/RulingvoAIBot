# handlers/practice_handler.py
"""
Free practice handler
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.operations import get_user, add_xp
from keyboards import get_back_keyboard
from services.ai_service import evaluate_text
from states import BotStates
from config import Config
import logging

logger = logging.getLogger(__name__)

practice_router = Router()


@practice_router.callback_query(F.data == "practice")
async def start_practice(callback: CallbackQuery, state: FSMContext):
    """Start free practice"""
    user = get_user(callback.from_user.id)

    text = """✍️ <b>Free Practice</b>

Write anything in Russian!
I'll help correct it.

<i>Start writing:</i>"""

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(user.language),
        parse_mode="HTML"
    )
    await state.set_state(BotStates.practice)
    await callback.answer()


@practice_router.message(StateFilter(BotStates.practice))
async def evaluate_practice(message: Message, state: FSMContext):
    """Evaluate practice text"""
    user = get_user(message.from_user.id)

    try:
        evaluation = await evaluate_text(message.text, user.level)

        xp = Config.XP_REWARDS["practice_session"]
        add_xp(message.from_user.id, xp)

        text = f"""📊 <b>Evaluation</b>

<b>Grammar:</b> {evaluation.get('grammar_score', 0)}/10
<b>Vocabulary:</b> {evaluation.get('vocabulary_score', 0)}/10

<b>Feedback:</b>
{evaluation.get('feedback', 'Good!')}

<b>Corrections:</b>
{evaluation.get('corrections', 'Keep practicing!')}

+{xp} XP!"""

        await message.answer(
            text,
            reply_markup=get_back_keyboard(user.language),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in evaluate_practice: {e}")
        await message.answer("Error evaluating text. Please try again.")