import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.migrations import run_migrations
from handlers import admin, tracker
from utils.system import configure_event_loop


logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(admin.router, tracker.router)

    logger.info("Бот запущен")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    configure_event_loop()
    run_migrations()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
