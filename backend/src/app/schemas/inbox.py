from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.quizzes import QuestionSchema, UserSchema


class InboxMessageSchema(BaseModel):
    question: QuestionSchema
    taker: UserSchema  # some fields may be hidden
    created_at: datetime


class InboxSchema(BaseModel):
    messages: List[InboxMessageSchema]
