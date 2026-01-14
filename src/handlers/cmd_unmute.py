from telethon import events

from ..database.requests import remove_from_ignore


def register_handler(client):
    @client.on(events.NewMessage(pattern=r'/unmute (.+)'))
    async def unmute_command(event):
        if not event.is_group and not event.is_channel:
            return None
        # TODO not is_admin

        target = event.pattern_match.group(1).strip()
        if not target:
            return await event.reply("Укажите ID или @username")

        try:
            user_to_unmute = await event.client.get_entity(target)
            await remove_from_ignore(event.chat_id, user_to_unmute.id)
            await event.reply(f"Пользователь {user_to_unmute.first_name} удален из исключений")
        except (ValueError, TypeError):
            await event.reply(f"Пользователь {target} не найден")
