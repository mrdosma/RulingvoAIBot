# services/audio_service.py - Audio & Voice Services
"""
Audio generation and voice recognition
Uses gTTS and Whisper API (OpenAI or Groq automatically)
"""

import asyncio
import logging
import os
from gtts import gTTS
import openai
from config import Config

# Try to import groq if available
try:
    from groq import Groq
except ImportError:
    Groq = None

logger = logging.getLogger(__name__)

# Detect available API
USE_GROQ = bool(os.getenv("GROQ_API_KEY")) and Groq is not None
if USE_GROQ:
    logger.info("Using Groq API for Whisper transcription.")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
else:
    openai.api_key = Config.OPENAI_API_KEY
    logger.info("Using OpenAI API for Whisper transcription.")


# ==================== AUDIO GENERATION ====================
async def generate_audio(text: str, filename: str = "audio.mp3") -> str:
    """Generate Russian audio from text using gTTS"""
    try:
        filepath = os.path.join(Config.AUDIO_DIR, filename)
        await asyncio.to_thread(_create_audio, text, filepath)
        logger.info(f"Audio generated: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Audio generation error: {e}")
        return None


def _create_audio(text: str, filepath: str):
    """Helper function to create audio (runs in thread)"""
    tts = gTTS(text=text, lang='ru', slow=False)
    tts.save(filepath)


# ==================== VOICE RECOGNITION ====================
async def transcribe_voice(file_path: str) -> str:
    """Transcribe voice message using Whisper API (Groq or OpenAI)"""
    try:
        with open(file_path, "rb") as audio_file:
            if USE_GROQ:
                # Groq version
                transcript = await asyncio.to_thread(
                    groq_client.audio.transcriptions.create,
                    model="whisper-large-v3",
                    file=audio_file
                )
                transcribed_text = transcript.text
            else:
                # OpenAI version
                transcript = await asyncio.to_thread(
                    openai.Audio.transcribe,
                    model=Config.WHISPER_MODEL,
                    file=audio_file,
                    language="ru"
                )
                transcribed_text = transcript.get("text", "")

        logger.info(f"Transcribed: {transcribed_text}")
        return transcribed_text

    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return ""


# ==================== FILE CLEANUP ====================
def cleanup_audio_file(filepath: str):
    """Delete audio file after use"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up: {filepath}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


def cleanup_old_files(directory: str, max_age_hours: int = 24):
    """Clean up old temporary files"""
    import time
    try:
        now = time.time()
        max_age_seconds = max_age_hours * 3600
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_age = now - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    logger.info(f"Cleaned up old file: {filepath}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
