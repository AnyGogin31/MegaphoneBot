from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    pass


class ChatMember(Base):
    __tablename__ = 'chat_members'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    is_ignored: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false())
