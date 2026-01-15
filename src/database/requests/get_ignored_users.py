from sqlalchemy import select

from .. import database_session
from ..models import IgnoredUsersModel


async def get_ignored_users(
    chat_id: int
) -> list[int]:
    stmt = (
        select(
            IgnoredUsersModel.user_id
        )
        .where(
            IgnoredUsersModel.chat_id == chat_id
        )
    )

    async with database_session() as session:
        result = await session.execute(stmt)
        return result.scalars().all()
