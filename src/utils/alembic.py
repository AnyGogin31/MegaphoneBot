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

from alembic import command
from alembic.config import Config

from .logging import get_logger
from ..configs import database_config


_logger = get_logger(__name__)


def configure_alembic() -> None:
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_config.url)
        command.upgrade(alembic_cfg, "head")
        _logger.debug("Миграции Alembic успешно применены")
    except Exception as e:
        _logger.debug("Ошибка при применении миграций Alembic: %s", e)
        _logger.critical("Критическая ошибка при обновлении базы данных")
        raise e
