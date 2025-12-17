from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.enums import ChatMemberStatus


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False

        member = await message.chat.get_member(message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]


class IsNotBot(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False

        return not message.from_user.is_bot


IsAdmin = IsAdmin()
IsNotBot = IsNotBot()
