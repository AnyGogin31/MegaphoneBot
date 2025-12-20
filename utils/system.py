import logging


logger = logging.getLogger(__name__)


def configure_event_loop():
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        logger.warning("uvloop не установлен")
    except Exception as e:
        logger.error(f"Ошибка при настройке uvloop: {e}")
