from datetime import datetime
from typing import List, Optional

from sqlalchemy import BIGINT, TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedAtMixin, TableNameMixin
from .users import User


class Group(Base, CreatedAtMixin, TableNameMixin):
    """
    This class represents a Group in the application.

    Attributes:
        group_id (Mapped[int]): The unique identifier of the group from Telegram.
        title (Mapped[str]): The name/title of the group.
        photo_url (Mapped[Optional[str]]): URL to the group's photo/avatar.
        creator_id (Mapped[int]): ID of the user who created the group.
        members (Mapped[List["GroupMember"]]): List of members in this group.
    """

    group_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(255))
    photo_url: Mapped[Optional[str]] = mapped_column(String(255))
    creator_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))

    # Relationships
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])
    members: Mapped[List["GroupMember"]] = relationship("GroupMember", back_populates="group")

    def __repr__(self):
        return f"<Group {self.group_id} {self.title}>"


class GroupMember(Base, CreatedAtMixin, TableNameMixin):
    """
    This class represents a Group Member in the application.

    Attributes:
        id (Mapped[int]): Primary key for the group member entry.
        group_id (Mapped[int]): The ID of the group.
        user_id (Mapped[int]): The ID of the user who is a member.
        is_admin (Mapped[bool]): Whether the user is an admin of the group.
    """

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("groups.group_id"))
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    is_admin: Mapped[bool] = mapped_column(default=False)

    # Relationships
    group: Mapped["Group"] = relationship("Group", back_populates="members")
    user: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"<GroupMember {self.user_id} in group {self.group_id}>"
