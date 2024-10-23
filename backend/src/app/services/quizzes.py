import random

from app.schemas.quizzes import (
    QuestionSchema,
    QuizListSchema,
    QuizResponseSchema,
    QuizSchema,
    UserSchema,
)
from app.services.base import BaseService


class QuizzesService(BaseService):
    async def get_random_quizzes(self, user_id: int, limit: int = 10) -> QuizListSchema:
        questions = await self.repo.questions.get_random_questions(limit)
        friends = await self.repo.users.get_friends(user_id)

        quizzes = [
            QuizSchema(
                question=QuestionSchema(id=q.id, text=q.text, emoji=q.emoji),
                friends=[
                    UserSchema(
                        id=f.user_id,
                        first_name=f.first_name,
                        last_name=f.last_name,
                        username=f.username,
                        photo_url=f.photo_url,
                    )
                    for f in random.sample(friends, 4)
                ],
            )
            for q in questions
        ]

        return QuizListSchema(quizzes=quizzes)

    async def create_quiz_response(self, user_id: int, request_data: dict) -> QuizResponseSchema:
        question_id = request_data.get("question_id")
        answer_id = request_data.get("answer_id")

        if not question_id or not answer_id:
            raise ValueError("Both question_id and answer_id are required")

        quiz_response = await self.repo.quiz_responses.create_quiz_response(
            taker_id=user_id, question_id=question_id, answer_id=answer_id
        )

        return QuizResponseSchema(
            id=quiz_response.id,
            taker_id=quiz_response.taker_id,
            question_id=quiz_response.question_id,
            answer_id=quiz_response.answer_id,
        )
