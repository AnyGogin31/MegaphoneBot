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
