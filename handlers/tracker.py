from aiogram import Router, F
from aiogram.types import Message
from database.requests import upsert_user


router = Router()
router.message.filter(F.chat.type.in_({'group', 'supergroup'}))


@router.message
async def capture_message(message: Message):
    if message.from_user and not message.from_user.is_bot:
        await upsert_user(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
