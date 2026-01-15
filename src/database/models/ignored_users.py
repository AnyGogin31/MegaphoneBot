from sqlalchemy import BigInteger
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from . import BaseModel


class IgnoredUsersModel(BaseModel):
    __tablename__ = "ignored_users"


    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
