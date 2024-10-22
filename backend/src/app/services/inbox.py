from app.schemas.inbox import InboxMessageSchema, InboxSchema
from app.schemas.questions import QuestionSchema
from app.schemas.users import UserSchema
from app.services.base import BaseService


class InboxService(BaseService):
    async def get_inbox_messages(self, user_id: int) -> InboxSchema:
        quiz_responses = await self.repo.quiz_responses.get_answers_for_user(user_id)

        inbox_messages = [
            InboxMessageSchema(
                question=QuestionSchema(
                    id=quiz_response.question.id,
                    text=quiz_response.question.text,
                    emoji=quiz_response.question.emoji,
                ),
                taker=UserSchema(
                    id=quiz_response.taker.user_id,
                    first_name=quiz_response.taker.first_name,
                    last_name=quiz_response.taker.last_name,
                    username=quiz_response.taker.username,
                    photo_url=quiz_response.taker.photo_url,
                ),
                created_at=quiz_response.created_at,
            )
            for quiz_response in quiz_responses
        ]

        return InboxSchema(messages=inbox_messages)
