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
