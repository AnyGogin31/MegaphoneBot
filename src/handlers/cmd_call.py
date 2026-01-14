from asyncio import sleep

from html import escape

from random import (
    choice,
    shuffle
)

from telethon import events

from ..database.requests import get_ignored_users


EMOJIS = [
    "🐸", "🐼", "🐭", "🦁", "🐮", "🐷", "🐨", "🐯", "🐙", "🐵",
    "🦄", "🐞", "🦀", "🐠", "🐊", "🐓", "🦃", "🐈", "🐕", "🦕",
    "🦖", "🦍", "🦧", "🦥", "🦦", "🦨", "🦘", "🦡", "🐘", "🍎",
    "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🥐",
    "🥯", "🥖", "🥨", "🥞", "🧇", "🧀", "🍖", "🍕", "🌭", "⚽",
    "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🎱", "⌚", "📱",
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"
]


def register_handler(client):
    @client.on(events.NewMessage(pattern=r'/call(?: (.+))?'))
    async def call_command(event):
        if not event.is_group and not event.is_channel:
            return None
        # TODO not is_admin

        ignored_users = await get_ignored_users(event.chat_id)
        all_users = await event.client.get_participants(event.chat_id)
        active_users = [
            user for user in all_users if not user.bot and user.id not in ignored_users
        ]

        if not active_users:
            return await event.reply("База пользователей пуста")

        reason_match = event.pattern_match.group(1)
        reason = escape(reason_match.strip()) if reason_match else "Йоу"

        mentions = []
        for user in active_users:
            random_emoji = choice(EMOJIS)
            link = f"<a href='tg://user?id={user.id}'>{random_emoji}</a>"
            mentions.append(link)

        shuffle(mentions)

        chunk_size = 10
        for i in range(0, len(mentions), chunk_size):
            chunk = mentions[i:i + chunk_size]
            mentions_text = " ".join(chunk)

            if i == 0:
                text = f"<b>{reason}</b>\n\n{mentions_text}"
            else:
                text = mentions_text

            await event.client.send_message(
                event.chat_id,
                text,
                parse_mode='html'
            )
            await sleep(0.5)

        return None
