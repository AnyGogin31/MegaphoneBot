from sqlalchemy import select, delete
from sqlalchemy.dialects.sqlite import insert
from database.models import ChatUser, ExceptionUser
from database.engine import async_session


async def upsert_user(user_id: int, chat_id: int, username: str, full_name: str):
    async with async_session() as session:
        stmt = insert(ChatUser).values(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
            full_name=full_name
        ).on_conflict_do_update(
            index_elements=['user_id', 'chat_id'],
            set_=dict(username=username, full_name=full_name)
        )
        await session.execute(stmt)
        await session.commit()


async def get_chat_users(chat_id: int):
    async with async_session() as session:
        result = await session.execute(select(ChatUser).where(ChatUser.chat_id == chat_id))
        return result.scalars().all()


async def add_exception(identifier: str, chat_id: int):
    async with async_session() as session:
        existing = await session.execute(
            select(ExceptionUser).where(
                ExceptionUser.identifier == identifier,
                ExceptionUser.chat_id == chat_id
            )
        )
        if not existing.scalar():
            session.add(ExceptionUser(identifier=identifier, chat_id=chat_id))
            await session.commit()


async def remove_exception(identifier: str, chat_id: int):
    async with async_session() as session:
        await session.execute(
            delete(ExceptionUser).where(
                ExceptionUser.identifier == identifier,
                ExceptionUser.chat_id == chat_id
            )
        )
        await session.commit()


async def get_exceptions(chat_id: int):
    async with async_session() as session:
        result = await session.execute(select(ExceptionUser.identifier).where(ExceptionUser.chat_id == chat_id))
        return result.scalars().all()
