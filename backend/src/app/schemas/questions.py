from typing import List

from pydantic import BaseModel, Field

from app.schemas.users import UserSchema


class QuestionSchema(BaseModel):
    id: int
    text: str
    emoji: str
