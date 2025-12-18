import asyncio
import logging
from alembic import command
from alembic.config import Config
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import admin, tracker


logger = logging.getLogger(__name__)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(admin.router, tracker.router)

    logger.info("Бот запущен")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        run_migrations()
    except Exception as e:
        logging.error(f"Ошибка при обновлении базы данных: {e}")
        exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
