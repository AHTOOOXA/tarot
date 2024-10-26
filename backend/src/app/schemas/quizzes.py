from typing import List

from pydantic import BaseModel, Field

from app.schemas.questions import QuestionSchema
from app.schemas.users import UserSchema


class QuizResponseSchema(BaseModel):
    taker_id: int
    question_id: int
    answer_id: int


class QuizSchema(BaseModel):
    question: QuestionSchema
    friends: List[UserSchema] = Field(..., min_items=4, max_items=4)


class QuizListSchema(BaseModel):
    quizzes: List[QuizSchema]
