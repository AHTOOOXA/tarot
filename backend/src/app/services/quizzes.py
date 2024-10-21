import random

from fastapi import Depends

from app.infrastructure.database.repo.requests import RequestsRepo
from app.schemas.quiz import QuestionSchema, QuizListSchema, QuizSchema, UserSchema
from app.webhook.dependencies.database import get_repo


class QuizzesService:
    def __init__(self, repo: RequestsRepo = Depends(get_repo)):
        self.repo = repo

    async def get_random_quizzes(self, user_id: int, limit: int = 10) -> QuizListSchema:
        questions = await self.repo.questions.get_random_questions(limit)
        friends = await self.repo.users.get_friends(user_id)

        quizzes = []
        for question in questions:
            quiz_friends = random.sample(friends, 4)
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
