import asyncio
import logging
from alembic import command
from alembic.config import Config
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import admin, tracker


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(tracker.router)

    print("Бот запущен")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run_migrations()
    except Exception as e:
        print(f"Ошибка при обновлении базы данных: {e}")
        exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
