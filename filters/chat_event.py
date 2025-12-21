from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter


OnUserJoin = ChatMemberUpdatedFilter(JOIN_TRANSITION)
OnUserLeft = ChatMemberUpdatedFilter(LEAVE_TRANSITION)
