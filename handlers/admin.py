import random
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatMemberStatus, ParseMode
from database.requests import get_chat_users, get_exceptions, add_exception, remove_exception


router = Router()


EMOJIS = [
    "🐸", "🐼", "🐭", "🦁", "🐮", "🐷", "🐨", "🐯", "🐙", "🐵",
    "🦄", "🐞", "🦀", "🐠", "🐊", "🐓", "🦃", "🐈", "🐕", "🦕",
    "🦖", "🦍", "🦧", "🦥", "🦦", "🦨", "🦘", "🦡", "🐘", "🍎",
    "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🥐",
    "🥯", "🥖", "🥨", "🥞", "🧇", "🧀", "🍖", "🍕", "🌭", "⚽",
    "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🎱", "⌚", "📱",
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"
]


def is_admin(message: Message) -> bool:
    return message.chat.type in ['group', 'supergroup']


async def check_admin_rights(message: Message):
    member = await message.chat.get_member(message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]


@router.message(Command("call"))
async def cmd_call(message: Message, command: CommandObject):
    if not await check_admin_rights(message):
        return await message.reply("Только администраторы могут вызывать всех")

    users = await get_chat_users(message.chat.id)
    exceptions = await get_exceptions(message.chat.id)

    if not users:
        return await message.reply("База пользователей пуста. Подождите, пока участники что-нибудь напишут")

    reason = command.args if command.args else "Йоу"

    mentions = []
    for user in users:
        str_id = str(user.user_id)
        u_name = f"@{user.username}" if user.username else None

        if str_id in exceptions:
            continue
        if u_name and u_name in exceptions:
            continue

        random_emoji = random.choice(EMOJIS)
        link = f"<a href='tg://user?id={user.user_id}'>{random_emoji}</a>"
        mentions.append(link)

    if not mentions:
        return await message.reply("Некого звать")

    random.shuffle(mentions)

    chunk_size = 10
    for i in range(0, len(mentions), chunk_size):
        chunk = mentions[i:i + chunk_size]
        mentions_text = " ".join(chunk)

        if i == 0:
            text = f"<b>{reason}</b>\n\n{mentions_text}"
        else:
            text = mentions_text

        await message.answer(text, parse_mode=ParseMode.HTML)
        await asyncio.sleep(0.5)

    return None


@router.message(Command("mute"))
async def cmd_mute(message: Message, command: CommandObject):
    if not await check_admin_rights(message):
        return None

    target = command.args
    if not target:
        return await message.reply("Используйте: /mute @username или ID")

    await add_exception(target.strip(), message.chat.id)
    await message.reply(f"Пользователь {target} добавлен в исключения")

    return None


@router.message(Command("unmute"))
async def cmd_unmute(message: Message, command: CommandObject):
    if not await check_admin_rights(message):
        return None

    target = command.args
    if not target:
        return await message.reply("Используйте: /unmute @username или ID")

    await remove_exception(target.strip(), message.chat.id)
    await message.reply(f"Пользователь {target} удален из исключений")

    return None
