#  MegaphoneBot
#  Copyright (C) 2026 AnyGogin31
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from telethon import TelegramClient

from .configs import api_config, bot_config
from .database import engine
from .handlers import register_handlers
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

    register_handlers(client)

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
