from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.database.models import User
from app.infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        is_bot: Optional[bool] = None,
        language_code: Optional[str] = None,
        is_premium: Optional[bool] = None,
        added_to_attachment_menu: Optional[bool] = None,
        allows_write_to_pm: Optional[bool] = None,
        photo_url: Optional[str] = None,
    ):
        """
        Creates or updates a user in the database and returns the user object.
        :param user_id: The user's ID.
        :param first_name: The user's first name.
        :param last_name: The user's last name.
        :param username: The user's username. It's an optional parameter.
        :param is_bot: Whether the user is a bot.
        :param language_code: The user's language code.
        :param is_premium: Whether the user is a premium user.
        :param added_to_attachment_menu: Whether the user is added to attachment menu.
        :param allows_write_to_pm: Whether the user allows write to PM.
        :param photo_url: The user's photo URL.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                is_bot=is_bot,
                language_code=language_code,
                is_premium=is_premium,
                added_to_attachment_menu=added_to_attachment_menu,
                allows_write_to_pm=allows_write_to_pm,
                photo_url=photo_url,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    is_bot=is_bot,
                    language_code=language_code,
                    is_premium=is_premium,
                    added_to_attachment_menu=added_to_attachment_menu,
                    allows_write_to_pm=allows_write_to_pm,
                    photo_url=photo_url,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()
