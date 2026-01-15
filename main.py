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
