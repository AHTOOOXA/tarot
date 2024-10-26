from app.schemas.inbox import InboxMessageSchema, InboxSchema
from app.schemas.questions import QuestionSchema
from app.schemas.users import UserSchema
from app.services.base import BaseService


class InboxService(BaseService):
    async def get_inbox_messages(self, user_id: int) -> InboxSchema:
        quiz_responses = await self.repo.quiz_responses.get_answers_for_user(user_id)

        inbox_messages = [
            InboxMessageSchema(
                question=QuestionSchema.model_validate(quiz_response.question),
                taker=UserSchema.model_validate(quiz_response.taker),
                created_at=quiz_response.created_at,
            )
            for quiz_response in quiz_responses
        ]

        return InboxSchema(messages=inbox_messages)
