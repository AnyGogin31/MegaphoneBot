from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert
from database.models import ChatMember
from database.engine import async_session


async def upsert_user(user_id: int, chat_id: int, username: str, full_name: str):
    async with async_session() as session:
        stmt = insert(ChatMember).values(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
            full_name=full_name,
            is_ignored=False,
            is_deleted=False
        ).on_conflict_do_update(
            index_elements=['user_id', 'chat_id'],
            set_=dict(
                username=username,
                full_name=full_name,
                is_deleted=False
            )
        )
        await session.execute(stmt)
        await session.commit()


async def get_active_users(chat_id: int):
    async with async_session() as session:
        stmt = select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.is_ignored == False,
            ChatMember.is_deleted == False
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def soft_delete_user(user_id: int, chat_id: int):
    async with async_session() as session:
        stmt = update(ChatMember).where(
            ChatMember.user_id == user_id,
            ChatMember.chat_id == chat_id
        ).values(is_deleted=True)
        await session.execute(stmt)
        await session.commit()


async def set_ignore_status(chat_id: int, identifier: str, is_ignored: bool) -> bool:
    async with async_session() as session:
        if identifier.isdigit():
            user_id = int(identifier)
            stmt = insert(ChatMember).values(
                user_id=user_id,
                chat_id=chat_id,
                is_ignored=is_ignored,
                full_name="Unknown",
                is_deleted=False
            ).on_conflict_do_update(
                index_elements=['user_id', 'chat_id'],
                set_=dict(is_ignored=is_ignored)
            )
            await session.execute(stmt)
            await session.commit()
            return True

        elif identifier.startswith("@"):
            clean_username = identifier.lstrip("@")
            stmt = update(ChatMember).where(
                ChatMember.chat_id == chat_id,
                ChatMember.username == clean_username
            ).values(is_ignored=is_ignored)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

        return False
