from telethon import events

from ..database.requests import remove_from_ignore


def register_unmute_command_handler(client):
    @client.on(events.NewMessage(pattern=r'^/unmute(?:@[\w_]+bot)?\s+([@]\w+|[-]?\d{5,})'))
    async def unmute_command(event):
        if not event.is_group and not event.is_channel:
            return None
        # TODO not is_admin

        target = event.pattern_match.group(1).strip()
        if not target:
            return await event.reply("Укажите ID или @username")

        try:
            user_id = await client.get_entity(target) if target.startswith('@') else int(target)
            await remove_from_ignore(event.chat_id, user_id)
            await event.reply(f"Пользователь удален из исключений")
        except (ValueError, TypeError):
            await event.reply(f"Пользователь {target} не найден")
