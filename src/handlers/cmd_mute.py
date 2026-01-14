from telethon import events


def register_handler(client):
    @client.on(events.NewMessage(pattern=r'/mute (.+)'))
    async def mute_command(event):
        if not event.is_group and not event.is_channel:
            return

        pass

