from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin


class Question(Base, TableNameMixin):
    """
    This class represents a Question in the application.

    Attributes:
        id (Mapped[int]): The unique identifier of the question.
        text (Mapped[str]): The text of the question.
        emoji (Mapped[str]): The emoji associated with the question.

    Methods:
        __repr__(): Returns a string representation of the Question object.

    Inherited Attributes:
        Inherits from Base, and TableNameMixin classes, which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, and TableNameMixin classes, which provide additional functionality.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    emoji: Mapped[str] = mapped_column(String(8), nullable=False)

    quiz_responses: Mapped[List["QuizResponse"]] = relationship("QuizResponse", back_populates="question")

    def __repr__(self):
        return f"<Question {self.id} {self.text[:20]}...>"
