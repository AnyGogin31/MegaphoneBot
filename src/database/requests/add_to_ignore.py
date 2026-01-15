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

from sqlalchemy.dialects.sqlite import insert

from .. import database_session
from ..models import IgnoredUsersModel


async def add_to_ignore(
    chat_id: int,
    user_id: int
):
    stmt = (
        insert(
            IgnoredUsersModel
        )
        .values(
            chat_id=chat_id,
            user_id=user_id
        )
        .on_conflict_do_nothing()
    )

    async with database_session() as session:
        await session.execute(stmt)
