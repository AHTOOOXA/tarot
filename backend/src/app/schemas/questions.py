from pydantic import BaseModel, ConfigDict


class QuestionSchema(BaseModel):
    id: int
    text: str
    emoji: str

    model_config = ConfigDict(from_attributes=True)
