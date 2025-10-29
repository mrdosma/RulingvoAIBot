# services/free_ai_service.py - BEPUL AI Alternativalar
"""
100% BEPUL AI variantlari
OpenAI o'rniga ishlatish mumkin
"""

import asyncio
import aiohttp
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# ==================== OPTION 1: GROQ (BEPUL, TEZKOR) ====================
"""
Groq - 100% BEPUL!
Llama 3.1 modelini ishlatadi (Meta tarafidan)
Juda tez va yaxshi

QANDAY ISHLATISH:
1. https://console.groq.com/ ga kiring
2. API key oling (BEPUL!)
3. .env ga qo'shing: GROQ_API_KEY=xxx
"""


async def groq_generate_text(prompt: str, system_message: str = "You are a helpful Russian language teacher.") -> str:
    """Groq API (BEPUL!)"""
    import os

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Groq API key not configured"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-70b-versatile",  # BEPUL!
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "AI temporarily unavailable"


# ==================== OPTION 2: HUGGINGFACE (BEPUL) ====================
"""
HuggingFace - 100% BEPUL!
Ko'plab modellar mavjud

QANDAY ISHLATISH:
1. https://huggingface.co/ ga kiring
2. API token oling (BEPUL!)
3. .env ga qo'shing: HUGGINGFACE_API_KEY=xxx
"""


async def huggingface_generate_text(prompt: str) -> str:
    """HuggingFace API (BEPUL!)"""
    import os

    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        return "HuggingFace API key not configured"

    # Yaxshi bepul model
    model = "meta-llama/Meta-Llama-3-8B-Instruct"
    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]["generated_text"]
                return str(result)
    except Exception as e:
        logger.error(f"HuggingFace API error: {e}")
        return "AI temporarily unavailable"


# ==================== OPTION 3: TOGETHER AI (ARZON) ====================
"""
Together AI - Juda arzon!
$0.0006 per 1000 tokens (100x arzonroq OpenAI dan!)

QANDAY ISHLATISH:
1. https://api.together.xyz/ ga kiring
2. $1 credit bepul beriladi
3. API key oling
4. .env ga qo'shing: TOGETHER_API_KEY=xxx
"""


async def together_generate_text(prompt: str,
                                 system_message: str = "You are a helpful Russian language teacher.") -> str:
    """Together AI (JUDA ARZON!)"""
    import os

    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        return "Together API key not configured"

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Together AI error: {e}")
        return "AI temporarily unavailable"


# ==================== OPTION 4: OLLAMA (100% BEPUL, LOCAL) ====================
"""
Ollama - O'z kompyuteringizda ishlatish!
100% BEPUL, internetga ulanish kerak emas!

QANDAY ISHLATISH:
1. https://ollama.com/ dan yuklab oling
2. O'rnating
3. Model yuklab oling: ollama pull llama3.1
4. Ishga tushiring: ollama serve
"""


async def ollama_generate_text(prompt: str, system_message: str = "You are a helpful Russian language teacher.") -> str:
    """Ollama (LOCAL, 100% BEPUL!)"""

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3.1",
        "prompt": f"{system_message}\n\nUser: {prompt}\n\nAssistant:",
        "stream": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                result = await response.json()
                return result["response"]
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return "Ollama not running. Start with: ollama serve"


# ==================== UNIFIED FUNCTION ====================
async def get_ai_response_free(
        prompt: str,
        system_message: str = "You are a helpful Russian language teacher.",
        provider: str = "groq"  # groq, huggingface, together, ollama
) -> str:
    """
    Unified function - istalgan bepul AI ni tanlang!

    Args:
        prompt: Savol
        system_message: Sistema xabari
        provider: AI provider (groq, huggingface, together, ollama)

    Returns:
        AI javobi
    """

    if provider == "groq":
        return await groq_generate_text(prompt, system_message)
    elif provider == "huggingface":
        return await huggingface_generate_text(prompt)
    elif provider == "together":
        return await together_generate_text(prompt, system_message)
    elif provider == "ollama":
        return await ollama_generate_text(prompt, system_message)
    else:
        return "Unknown AI provider"


# ==================== VOCABULARY GENERATION (BEPUL) ====================
async def generate_vocabulary_free(level: str, count: int = 5, provider: str = "groq") -> List[Dict]:
    """Generate vocabulary using FREE AI"""

    prompt = f"""Generate {count} Russian vocabulary words for {level} level.
Return as JSON array:
[{{"word": "...", "translation": "...", "example": "..."}}]"""

    response = await get_ai_response_free(prompt, provider=provider)

    try:
        import json
        # Clean response
        response = response.strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]

        return json.loads(response)
    except:
        # Fallback
        return [
            {"word": "привет", "translation": "hello", "example": "Привет! Как дела?"},
            {"word": "спасибо", "translation": "thank you", "example": "Спасибо за помощь!"}
        ]


# ==================== EVALUATION (BEPUL) ====================
async def evaluate_text_free(text: str, level: str, provider: str = "groq") -> Dict:
    """Evaluate Russian text using FREE AI"""

    prompt = f"""Evaluate this Russian text from a {level} learner: "{text}"
Return JSON: {{"grammar_score": 1-10, "vocabulary_score": 1-10, "feedback": "...", "corrections": "..."}}"""

    response = await get_ai_response_free(prompt, provider=provider)

    try:
        import json
        response = response.strip()
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]

        return json.loads(response)
    except:
        return {
            "grammar_score": 7,
            "vocabulary_score": 7,
            "feedback": "Good effort!",
            "corrections": "Keep practicing!"
        }


# ==================== BACKWARDS-COMPATIBILITY WRAPPERS ====================
async def generate_grammar_exercise(level: str, provider: str = "groq") -> Dict:
    """Compatibility wrapper: generate a simple grammar exercise JSON using the free AI functions."""
    prompt = (
        f"Create a short grammar exercise for a {level} Russian learner.\n"
        '{"Return JSON with keys": {"question": "...", "answer": "...", "rule": "...", "example": "..."}}'
    )

    response = await get_ai_response_free(prompt, provider=provider)

    try:
        import json
        # attempt to extract JSON from the response
        text = response.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text)
    except Exception:
        # fallback simple exercise
        return {
            "question": "Fill the blank: Я ___ (to be) студент.",
            "answer": "есть",
            "rule": "Use the verb 'to be' in present tense where appropriate.",
            "example": "Он студент. Я студент."
        }


async def evaluate_text(text: str, level: str, provider: str = "groq") -> Dict:
    """Compatibility wrapper: delegate to evaluate_text_free."""
    return await evaluate_text_free(text, level, provider=provider)


async def generate_listening_text(level: str, provider: str = "groq") -> str:
    """Generate a short listening sentence for the given level."""
    prompt = f"Generate one short Russian sentence appropriate for a {level} learner. Return only the sentence." 

    response = await get_ai_response_free(prompt, provider=provider)
    # Attempt to extract simple text
    text = response.strip()
    # remove code fences if present
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1].strip()
    return text


async def generate_conversation_prompt(level: str, provider: str = "groq") -> str:
    """Generate a starter prompt/question for a speaking duel at the given level."""
    prompt = f"Provide one short conversational prompt in Russian suitable for a {level} learner. Return only the prompt sentence."
    response = await get_ai_response_free(prompt, provider=provider)
    return response.strip()


async def generate_conversation_response(level: str, user_text: str, provider: str = "groq") -> str:
    """Generate an AI reply in Russian to the user's message for the speaking duel."""
    prompt = (
        f"You are an AI conversation partner for a {level} Russian learner. Reply in Russian to the user's message below.\nUser: {user_text}\nAI:"
    )
    response = await get_ai_response_free(prompt, provider=provider)
    return response.strip()


async def generate_spy_mission(level: str, provider: str = "groq") -> str:
    """Generate a short spy mission prompt (in Russian) appropriate for the learner level."""
    prompt = f"Create a short 'spy mission' instruction in Russian appropriate for a {level} learner. Return only the instruction text." 
    response = await get_ai_response_free(prompt, provider=provider)
    return response.strip()