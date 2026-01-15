from telethon import events

from ..database.requests import add_to_ignore


def register_mute_command_handler(client):
    @client.on(events.NewMessage(pattern=r'^/mute(?:@[\w_]+bot)?\s+([@]\w+|[-]?\d{5,})'))
    async def mute_command(event):
        if not event.is_group and not event.is_channel:
            return None
        # TODO not is_admin

        target = event.pattern_match.group(1).strip()
        if not target:
            return await event.reply("Укажите ID или @username")

        try:
            user_id = await client.get_entity(target) if target.startswith('@') else int(target)
            await add_to_ignore(event.chat_id, user_id)
            await event.reply(f"Пользователь добавлен в исключения")
        except (ValueError, TypeError):
            await event.reply(f"Пользователь {target} не найден")
