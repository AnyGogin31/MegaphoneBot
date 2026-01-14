from sqlalchemy import delete

from .. import database_session
from ..models import IgnoredUsersModel


async def remove_from_ignore(
    chat_id: int,
    user_id: int
):
    stmt = (
        delete(
            IgnoredUsersModel
        )
        .where(
            IgnoredUsersModel.chat_id == chat_id,
            IgnoredUsersModel.user_id == user_id
        )
    )

    async with database_session() as session:
        await session.execute(stmt)
