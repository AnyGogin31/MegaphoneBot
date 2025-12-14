import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import create_db
from handlers import admin, tracker


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(tracker.router)

    await create_db()

    print("Бот запущен")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
