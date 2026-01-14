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
