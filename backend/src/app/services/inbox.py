from fastapi import Depends

from app.infrastructure.database.repo.requests import RequestsRepo
from app.schemas.inbox import InboxMessageSchema, InboxSchema
from app.webhook.dependencies.database import get_repo


class InboxService:
    def __init__(self, repo: RequestsRepo = Depends(get_repo)):
        self.repo = repo

    async def get_inbox_messages(self, user_id: int) -> InboxSchema:
        quiz_responses = await self.repo.quiz_responses.get_quiz_responses_by_taker(user_id)
        inbox_messages = [
            InboxMessageSchema(
                question=quiz_response.question,
                taker=quiz_response.taker,
                created_at=quiz_response.created_at,
            )
            for quiz_response in quiz_responses
        ]
        return InboxSchema(messages=inbox_messages)
