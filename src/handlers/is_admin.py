from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

async def is_admin(
    client,
    user_id,
    chat_id
):
    try:
        participant = await client(
            GetParticipantRequest(
                channel=chat_id,
                participant=user_id
            )
        )
        return isinstance(
            participant.participant,
            (ChannelParticipantAdmin, ChannelParticipantCreator)
        )
    except Exception:
        return False
