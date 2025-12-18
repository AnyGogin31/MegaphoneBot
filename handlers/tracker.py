from aiogram import Router
from aiogram.types import Message
from database.requests import upsert_user
from filters.chat_type import IsGroup
from filters.user_status import IsNotBot


router = Router()
router.message.filter(IsGroup, IsNotBot)


@router.message()
async def capture_message(message: Message):
    await upsert_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
