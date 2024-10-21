from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repo import RequestsRepo
from app.schemas.quizzes import QuestionSchema, QuizListSchema, QuizSchema, UserSchema


class QuizzesService:
    def __init__(self, repo: RequestsRepo):
        self.repo = repo

    async def get_random_quizzes(self, session: AsyncSession, user_id: int, limit: int = 10) -> QuizListSchema:
        questions = await self.repo.questions.get_random_questions(session, limit)
        friends = await self.repo.users.get_friends(session, user_id)

        quizzes = []
        for question in questions:
            quiz_friends = self._get_random_friends(friends, 4)
            quiz = QuizSchema(
                question=QuestionSchema(id=question.id, text=question.text, emoji=question.emoji),
                friends=[
                    UserSchema(
                        id=friend.user_id,
                        first_name=friend.first_name,
                        last_name=friend.last_name,
                        username=friend.username,
                        photo_url=friend.photo_url,
                    )
                    for friend in quiz_friends
                ],
            )
            quizzes.append(quiz)

        return QuizListSchema(quizzes=quizzes)
