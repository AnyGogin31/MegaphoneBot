from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from database.requests import upsert_user, soft_delete_user
from filters.chat_event import OnUserLeft, OnUserJoin
from filters.chat_type import IsGroup
from filters.user_status import IsNotBot


router = Router()
router.message.filter(IsGroup, IsNotBot)
router.chat_member.filter(IsGroup)


@router.chat_member(OnUserJoin)
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    if not user.is_bot:
        await upsert_user(
            user_id=user.id,
            chat_id=event.chat.id,
            username=user.username,
            full_name=user.full_name
        )


@router.chat_member(OnUserLeft)
async def on_user_leave(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    if not user.is_bot:
        await soft_delete_user(
            user_id=user.id,
            chat_id=event.chat.id
        )


@router.message()
async def capture_message(message: Message):
    await upsert_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
