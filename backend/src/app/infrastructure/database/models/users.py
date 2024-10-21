from typing import List, Optional

from sqlalchemy import BIGINT, Boolean, String, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin, TimestampMixin


class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a User in the application.
    If you want to learn more about SQLAlchemy and Alembic, you can check out the following link to my course:
    https://www.udemy.com/course/sqlalchemy-alembic-bootcamp/?referralCode=E9099C5B5109EB747126

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        first_name (Mapped[str]): The first name of the user.
        last_name (Mapped[Optional[str]]): The last name of the user.
        username (Mapped[Optional[str]]): The username of the user.
        is_bot (Mapped[Optional[bool]]): Whether the user is a bot.
        language_code (Mapped[Optional[str]]): The user's language code.
        is_premium (Mapped[Optional[bool]]): Whether the user is a premium user.
        added_to_attachment_menu (Mapped[Optional[bool]]): Whether the user is added to attachment menu.
        allows_write_to_pm (Mapped[Optional[bool]]): Whether the user allows write to PM.
        photo_url (Mapped[Optional[str]]): The user's photo URL.
        friendships (Mapped[List["Friendship"]]): List of friendships associated with this user.
        taken_quizzes (Mapped[List["QuizResponse"]]): List of quiz responses where this user is the taker.
        answered_quizzes (Mapped[List["QuizResponse"]]): List of quiz responses where this user is the answer.

    Methods:
        __repr__(): Returns a string representation of the User object.

    Inherited Attributes:
        Inherits from Base, TimestampMixin, and TableNameMixin classes, which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, TimestampMixin, and TableNameMixin classes, which provide additional functionality.
    """

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

    friendships: Mapped[List["Friendship"]] = relationship(
        "Friendship",
        primaryjoin="or_(User.user_id==Friendship.user_id1, User.user_id==Friendship.user_id2)",
        viewonly=True,
    )

    taken_quizzes: Mapped[List["QuizResponse"]] = relationship(
        "QuizResponse", foreign_keys="[QuizResponse.taker_id]", back_populates="taker"
    )
    answered_quizzes: Mapped[List["QuizResponse"]] = relationship(
        "QuizResponse", foreign_keys="[QuizResponse.answer_id]", back_populates="answer"
    )

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.first_name} {self.last_name}>"
