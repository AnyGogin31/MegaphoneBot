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

from telethon import events

from .is_admin import is_admin
from ..database.requests import add_to_ignore


def register_mute_command_handler(client):
    @client.on(events.NewMessage(pattern=r'^/mute(?:@[\w_]+bot)?\s+([@]\w+|[-]?\d{5,})'))
    async def mute_command(event):
        if not event.is_group and not event.is_channel:
            return
        if not await is_admin(event.client, event.sender_id, event.chat_id):
            return

        target = event.pattern_match.group(1).strip()
        if not target:
            await event.reply("Укажите ID или @username")
            return

        try:
            user_id = await client.get_entity(target) if target.startswith('@') else int(target)
            await add_to_ignore(event.chat_id, user_id)
            await event.reply(f"Пользователь добавлен в исключения")
        except (ValueError, TypeError):
            await event.reply(f"Пользователь {target} не найден")
