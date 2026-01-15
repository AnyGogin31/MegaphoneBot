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
