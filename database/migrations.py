import logging
from alembic import command
from alembic.config import Config


logger = logging.getLogger(__name__)


def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("База данных успешно обновлена")
    except Exception as e:
        logger.critical(f"Ошибка при обновлении базы данных: {e}")
        raise e
