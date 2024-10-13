from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.database.models import Question
from app.infrastructure.database.repo.base import BaseRepo


class QuestionRepo(BaseRepo):
    async def create_question(
        self,
        text: str,
        emoji: str,
    ) -> Question:
        """
        Creates a new question in the database and returns the question object.
        :param text: The text of the question.
        :param emoji: The emoji associated with the question.
        :return: Question object.
        """
        insert_stmt = (
            insert(Question)
            .values(
                text=text,
                emoji=emoji,
            )
            .returning(Question)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """
        Retrieves a question from the database by its ID.
        :param question_id: The ID of the question to retrieve.
        :return: Question object if found, None otherwise.
        """
        query = select(Question).where(Question.id == question_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_questions(self) -> List[Question]:
        """
        Retrieves all questions from the database.
        :return: List of Question objects.
        """
        query = select(Question)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_random_questions(self, limit: int = 10) -> List[Question]:
        """
        Retrieves a specified number of random questions from the database.
        :param limit: The number of questions to retrieve (default: 10)
        :return: List of Question objects.
        """
        query = select(Question).order_by(func.random()).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
