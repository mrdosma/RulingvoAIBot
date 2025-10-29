# bot.py - Main Entry Point
"""
Russian Learner Bot - Main Application
This is the main entry point that starts the bot
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from database.models import init_db
from handlers import router
from scheduler import setup_scheduler

# Logging setup
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_startup():
    """Run on bot startup"""
    logger.info("Bot starting...")

    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Setup scheduler for notifications
    await setup_scheduler(bot)
    logger.info("Scheduler initialized")

    logger.info("Bot started successfully!")


async def on_shutdown():
    """Run on bot shutdown"""
    logger.info("Bot shutting down...")
    await bot.session.close()
    logger.info("Bot stopped")


async def main():
    """Main function"""
    try:
        # Register router
        dp.include_router(router)

        # Register startup/shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        # Start polling
        logger.info("Starting polling...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Russian Learner Bot Starting...")
    print("=" * 50)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)