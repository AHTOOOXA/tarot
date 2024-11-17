from datetime import date
from typing import List, Optional

from sqlalchemy import BIGINT, Boolean, Date, String, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedAtMixin, TableNameMixin, UpdatedAtMixin


class User(Base, CreatedAtMixin, UpdatedAtMixin, TableNameMixin):
    # Telegram user fields
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[Optional[str]] = mapped_column(String(64))
    username: Mapped[Optional[str]] = mapped_column(String(32))
    is_bot: Mapped[Optional[bool]] = mapped_column(Boolean)
    language_code: Mapped[Optional[str]] = mapped_column(String(8))
    is_premium: Mapped[Optional[bool]] = mapped_column(Boolean)
    added_to_attachment_menu: Mapped[Optional[bool]] = mapped_column(Boolean)
    allows_write_to_pm: Mapped[Optional[bool]] = mapped_column(Boolean)
    photo_url: Mapped[Optional[str]] = mapped_column(String(255))

    # App user fields
    app_username: Mapped[Optional[str]] = mapped_column(String(128))
    app_language_code: Mapped[str] = mapped_column(String, default="en")
    male: Mapped[Optional[bool]] = mapped_column(Boolean)
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    is_onboarded: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    friendships: Mapped[List["Friendship"]] = relationship(
        "Friendship",
        primaryjoin="or_(User.user_id==Friendship.user_id1, User.user_id==Friendship.user_id2)",
        viewonly=True,
    )

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.first_name} {self.last_name}>"
