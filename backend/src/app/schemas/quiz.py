from typing import List

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None


class QuestionSchema(BaseModel):
    id: int
    text: str
    emoji: str


class QuizSchema(BaseModel):
    question: QuestionSchema
    friends: List[UserSchema] = Field(..., min_items=4, max_items=4)


class QuizResponseSchema(BaseModel):
    id: int
    taker_id: int
    question_id: int
    answer_id: int


class QuizListSchema(BaseModel):
    quizzes: List[QuizSchema]


class QuizStatsSchema(BaseModel):
    quizzes_taken: int
    times_answered: int
    question_stats: dict[int, dict[str, int | float]]


class LatestResponsesSchema(BaseModel):
    responses: List[QuizResponseSchema]
