from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from ..configs import database_config
from ..utils.logging import get_logger


_logger = get_logger(__name__)


engine = create_async_engine(
    url=database_config.url,
    echo=False
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def database_session():
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        _logger.debug("Ошибка при выполнении операции с базой данных: %s", e)
        _logger.critical("Критическая ошибка при выполнении операции с базой данных")
    finally:
        await session.close()
