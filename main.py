import asyncio

from src.bot import start_bot
from src.utils.alembic import configure_alembic
from src.utils.logging import configure_logging
from src.utils.uvloop import configure_uvloop


def main():
    configure_logging()
    configure_uvloop()
    configure_alembic()

    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
