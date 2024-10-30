import random
from typing import List

from app.schemas.quizzes import (
    QuestionSchema,
    QuizResponseSchema,
    QuizSchema,
    UserSchema,
)
from app.services.base import BaseService


class QuizzesService(BaseService):
    async def get_random_quizzes(self, user_id: int, limit: int = 10) -> List[QuizSchema]:
        questions = await self.repo.questions.get_random_questions(limit)
        friends = await self.repo.users.get_friends(user_id)

        quizzes = [
            QuizSchema(
                question=QuestionSchema.model_validate(q),
                friends=[UserSchema.model_validate(f) for f in random.sample(friends, 4)],
            )
            for q in questions
        ]

        return quizzes

    async def create_quiz_response(self, quiz_response: QuizResponseSchema) -> None:
        quiz_response = await self.repo.quiz_responses.create_quiz_response(
            taker_id=quiz_response.taker_id,
            question_id=quiz_response.question_id,
            answer_id=quiz_response.answer_id,
        )
        question = await self.repo.questions.get_question_by_id(quiz_response.question_id)
        await self.producer.publish(
            {
                "user_id": quiz_response.answer_id,
                "text": f"Someone answered a quiz about: '{question.text}'",
            }
        )
