#  MegaphoneBot
#  Copyright (C) 2026 AnyGogin31
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from asyncio import sleep

from html import escape

from random import (
    choice,
    shuffle
)

from telethon import events

from .is_admin import is_admin
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


def register_call_command_handler(client):
    @client.on(events.NewMessage(pattern=r'^/call(?:@[\w_]+bot)?(?:\s+(.+))?$'))
    async def call_command(event):
        if not event.is_group and not event.is_channel:
            return
        if not await is_admin(event.client, event.sender_id, event.chat_id):
            return

        ignored_users = await get_ignored_users(event.chat_id)
        all_users = await event.client.get_participants(event.chat_id)
        active_users = [
            user for user in all_users if not user.bot and user.id not in ignored_users
        ]

        topic_id = get_topic_id(event.message)

        if not active_users:
            await event.reply("База пользователей пуста")
            return

        reason_match = event.pattern_match.group(1)
        reason = escape(reason_match.strip()) if reason_match else None
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
            if reason:
                text = f"<b>{reason}</b>\n\n{mentions_text}"
            else:
                text = mentions_text

            await event.client.send_message(
                event.chat_id,
                text,
                parse_mode='html',
                reply_to=topic_id
            )
            await sleep(0.5)
