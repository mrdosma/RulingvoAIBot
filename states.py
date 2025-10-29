# states.py - FSM States
"""
Finite State Machine states for bot
"""

from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    """All bot states"""

    # General
    selecting_language = State()
    main_menu = State()

    # Vocabulary
    vocabulary_menu = State()
    flashcard_review = State()

    # Grammar
    grammar_exercise = State()

    # Listening
    listening_exercise = State()

    # Practice
    practice = State()

    # Games
    speaking_duel = State()
    spy_mission = State()
    word_game = State()