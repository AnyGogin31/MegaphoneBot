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
