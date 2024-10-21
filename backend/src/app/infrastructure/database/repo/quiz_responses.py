from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.quiz_response import QuizResponse
from app.infrastructure.database.repo.base import BaseRepo


class QuizResponsesRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_quiz_response(self, taker_id: int, question_id: int, answer_id: int) -> QuizResponse:
        """
        Create a new quiz response.

        Args:
            taker_id (int): The ID of the user taking the quiz.
            question_id (int): The ID of the question being answered.
            answer_id (int): The ID of the selected answer (user).

        Returns:
            QuizResponse: The created quiz response object.
        """
        quiz_response = QuizResponse(taker_id=taker_id, question_id=question_id, answer_id=answer_id)
        self.session.add(quiz_response)
        await self.session.commit()
        await self.session.refresh(quiz_response)
        return quiz_response

    async def get_quiz_responses_by_taker(self, taker_id: int) -> list[QuizResponse]:
        """
        Get all quiz responses for a specific taker.

        Args:
            taker_id (int): The ID of the user whose responses we want to retrieve.

        Returns:
            list[QuizResponse]: A list of QuizResponse objects for the given taker.
        """
        query = select(QuizResponse).where(QuizResponse.taker_id == taker_id)
        result = await self.session.execute(query)
        return result.scalars().all()
