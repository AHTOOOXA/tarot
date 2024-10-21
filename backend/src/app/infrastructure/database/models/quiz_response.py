from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin, TimestampMixin
from .questions import Question
from .users import User


class QuizResponse(Base, TableNameMixin, TimestampMixin):
    """
    This class represents a Quiz Response in the application.

    Attributes:
        id (Mapped[int]): The unique identifier of the quiz response.
        taker_id (Mapped[int]): The ID of the user who took the quiz.
        question_id (Mapped[int]): The ID of the question that was answered.
        answer_id (Mapped[int]): The ID of the user who was selected as the answer.
        taker (Mapped[User]): The relationship to the User model for the quiz taker.
        question (Mapped[Question]): The relationship to the Question model.
        answer (Mapped[User]): The relationship to the User model for the answer.

    Methods:
        __repr__(): Returns a string representation of the QuizResponse object.

    Inherited Attributes:
        Inherits from Base, TableNameMixin, and TimestampMixin classes, which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, TableNameMixin, and TimestampMixin classes, which provide additional functionality.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    taker_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)

    taker: Mapped[User] = relationship("User", foreign_keys=[taker_id], back_populates="taken_quizzes")
    question: Mapped[Question] = relationship("Question", back_populates="quiz_responses")
    answer: Mapped[User] = relationship("User", foreign_keys=[answer_id], back_populates="answered_quizzes")

    def __repr__(self):
        return f"<QuizResponse {self.id} Taker:{self.taker_id} Question:{self.question_id} Answer:{self.answer_id}>"
