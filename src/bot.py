from telethon import TelegramClient

from .configs import api_config, bot_config
from .database import engine
from .utils.logging import get_logger


_logger = get_logger(__name__)


async def create_client() -> TelegramClient:
    api_id = api_config.id.get_secret_value()
    api_hash = api_config.hash.get_secret_value()
    bot_token = bot_config.token.get_secret_value()

    client = await (
        TelegramClient(
            'megaphone-bot',
            api_id,
            api_hash
        )
        .start(
            bot_token=bot_token
        )
    )

    return client


async def start_bot():
    _logger.info("Запуск бота...")

    client = await create_client()

    try:
        _logger.info("Бот запущен")
        await client.run_until_disconnected()
    except Exception as e:
        _logger.debug("Ошибка во время работы бота: %s", e)
        _logger.critical("Бот аварийно завершил работу")
    finally:
        _logger.info("Остановка бота...")
        await client.disconnect()
        await engine.dispose()
        _logger.info("Бот остановлен")
