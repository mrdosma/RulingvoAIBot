# handlers/__init__.py - YANGILANGAN VERSIYA
"""
Main router combining all handlers
"""

from aiogram import Router

from handlers.start_handler import start_router
from handlers.menu_handler import menu_router
from handlers.vocabulary_handler import vocabulary_router
from handlers.grammar_handler import grammar_router
from handlers.listening_handler import listening_router
from handlers.practice_handler import practice_router
from handlers.games_handler import games_router
from handlers.profile_handler import profile_router
from handlers.settings_handler import settings_router

# Main router combining all handlers
router = Router()

# Include all sub-routers in correct order
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(profile_router)
router.include_router(vocabulary_router)
router.include_router(grammar_router)
router.include_router(listening_router)
router.include_router(practice_router)
router.include_router(games_router)
router.include_router(settings_router)

# Export for use in bot.py
__all__ = ['router']