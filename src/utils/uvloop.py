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

from .logging import get_logger


_logger = get_logger(__name__)


def configure_uvloop() -> None:
    try:
        import uvloop
        uvloop.install()
        _logger.debug("uvloop успешно активирован")
    except ImportError:
        _logger.debug("Модуль uvloop не найден в окружении")
    except Exception as e:
        _logger.debug("Не удалось активировать uvloop: %s", e)
