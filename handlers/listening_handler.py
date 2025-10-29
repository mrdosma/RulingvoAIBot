# handlers/listening_handler.py
"""
Listening exercises handler
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database.operations import get_user, add_xp
from keyboards import get_listening_keyboard, get_back_keyboard
from services.ai_service import generate_listening_text
from services.audio_service import generate_audio, cleanup_audio_file
from states import BotStates
from config import Config
import logging
import os

logger = logging.getLogger(__name__)

listening_router = Router()


@listening_router.callback_query(F.data == "listening")
async def start_listening(callback: CallbackQuery, state: FSMContext):
    """Start listening exercise"""
    user = get_user(callback.from_user.id)
    await callback.answer("Generating audio...")

    try:
        sentence = await generate_listening_text(user.level)
        audio_file = await generate_audio(sentence, f"listen_{callback.from_user.id}.mp3")

        if audio_file and os.path.exists(audio_file):
            await state.update_data(listening_answer=sentence)

            await callback.message.answer_audio(
                audio=FSInputFile(audio_file),
                caption="🎧 <b>Listening Exercise</b>\n\nListen and write what you hear:",
                reply_markup=get_listening_keyboard(user.language),
                parse_mode="HTML"
            )
            await state.set_state(BotStates.listening_exercise)

            # Cleanup
            cleanup_audio_file(audio_file)
        else:
            await callback.answer("Error generating audio")

    except Exception as e:
        logger.error(f"Error in start_listening: {e}")
        await callback.answer("Error. Please try again.")


@listening_router.callback_query(F.data == "listening_replay")
async def replay_listening(callback: CallbackQuery, state: FSMContext):
    """Replay audio"""
    await start_listening(callback, state)


@listening_router.message(StateFilter(BotStates.listening_exercise))
async def check_listening(message: Message, state: FSMContext):
    """Check listening answer"""
    data = await state.get_data()
    correct = data.get("listening_answer", "")

    # Simple similarity check
    user_words = set(message.text.lower().split())
    correct_words = set(correct.lower().split())

    if len(user_words) == 0 or len(correct_words) == 0:
        similarity = 0
    else:
        similarity = len(user_words & correct_words) / max(len(user_words), len(correct_words))

    is_correct = similarity > 0.6
    xp = Config.XP_REWARDS["listening_exercise"] if is_correct else 15
    add_xp(message.from_user.id, xp)

    result = "✅ Correct!" if is_correct else "❌ Close!"
    text = f"""{result}

<b>You wrote:</b> {message.text}
<b>Correct:</b> {correct}
<b>Similarity:</b> {similarity * 100:.0f}%

+{xp} XP!"""

    await message.answer(text, parse_mode="HTML")
    await state.clear()