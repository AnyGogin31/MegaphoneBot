import html
import random
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode
from database.requests import get_active_users, set_ignore_status
from filters.chat_type import IsGroup
from filters.user_status import IsAdmin


router = Router()
router.message.filter(IsGroup, IsAdmin)


EMOJIS = [
    "🐸", "🐼", "🐭", "🦁", "🐮", "🐷", "🐨", "🐯", "🐙", "🐵",
    "🦄", "🐞", "🦀", "🐠", "🐊", "🐓", "🦃", "🐈", "🐕", "🦕",
    "🦖", "🦍", "🦧", "🦥", "🦦", "🦨", "🦘", "🦡", "🐘", "🍎",
    "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🥐",
    "🥯", "🥖", "🥨", "🥞", "🧇", "🧀", "🍖", "🍕", "🌭", "⚽",
    "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🎱", "⌚", "📱",
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"
]


@router.message(Command("call"))
async def cmd_call(message: Message, command: CommandObject):
    users_ids = await get_active_users(message.chat.id)

    if not users_ids:
        return await message.reply("База пользователей пуста")

    reason = html.escape(command.args) if command.args else "Йоу"

    mentions = []
    for user_id in users_ids:
        random_emoji = random.choice(EMOJIS)
        link = f"<a href='tg://user?id={user_id}'>{random_emoji}</a>"
        mentions.append(link)

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
    target = command.args
    if not target:
        return await message.reply("Укажите ID или @username")

    success = await set_ignore_status(message.chat.id, target.strip(), is_ignored=True)
    if success:
        await message.reply(f"Пользователь {target} добавлен в исключения")
    else:
        await message.reply(f"Пользователь {target} не найден")

    return None


@router.message(Command("unmute"))
async def cmd_unmute(message: Message, command: CommandObject):
    target = command.args
    if not target:
        return await message.reply("Укажите ID или @username")

    success = await set_ignore_status(message.chat.id, target.strip(), is_ignored=False)

    if success:
        await message.reply(f"Пользователь {target} удален из исключений")
    else:
        await message.reply(f"Пользователь {target} не найден")

    return None
