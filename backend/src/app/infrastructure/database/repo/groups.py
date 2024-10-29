from typing import List, Optional

from sqlalchemy import delete, select

from ..models.groups import Group, GroupMember
from ..models.users import User
from .base import BaseRepo


class GroupRepo(BaseRepo):
    async def create_group(self, group_id: int, title: str, creator_id: int, photo_url: Optional[str] = None) -> Group:
        """
        Create a new group and add the creator as an admin member.

        Args:
            group_id: Telegram group ID
            title: Group title
            creator_id: User ID of the group creator
            photo_url: Optional URL to group photo

        Returns:
            Group: The created group instance
        """
        # Create the group
        group = Group(group_id=group_id, title=title, creator_id=creator_id, photo_url=photo_url)
        self.session.add(group)
        await self.session.flush()

        # Add creator as admin member
        member = GroupMember(group_id=group_id, user_id=creator_id, is_admin=True)
        self.session.add(member)
        await self.session.flush()

        return group

    async def add_member(self, group_id: int, user_id: int, is_admin: bool = False) -> GroupMember:
        """
        Add a user to a group.

        Args:
            group_id: ID of the group
            user_id: ID of the user to add
            is_admin: Whether the user should be added as an admin

        Returns:
            GroupMember: The created group member instance
        """
        # Check if user is already a member
        existing = await self.session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        if existing.scalar_one_or_none():
            raise ValueError("User is already a member of this group")

        member = GroupMember(group_id=group_id, user_id=user_id, is_admin=is_admin)
        self.session.add(member)
        await self.session.flush()
        return member

    async def remove_member(self, group_id: int, user_id: int) -> None:
        """
        Remove a user from a group.

        Args:
            group_id: ID of the group
            user_id: ID of the user to remove
        """
        await self.session.execute(
            delete(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        await self.session.flush()

    async def get_group(self, group_id: int) -> Optional[Group]:
        """
        Get a group by its ID.

        Args:
            group_id: The group ID to look up

        Returns:
            Optional[Group]: The group if found, None otherwise
        """
        result = await self.session.execute(select(Group).where(Group.group_id == group_id))
        return result.scalar_one_or_none()

    async def get_group_members(self, group_id: int) -> List[User]:
        """
        Get all members of a group.

        Args:
            group_id: The group ID to get members for

        Returns:
            List[User]: List of users who are members of the group
        """
        result = await self.session.execute(
            select(User).join(GroupMember, GroupMember.user_id == User.user_id).where(GroupMember.group_id == group_id)
        )
        return list(result.scalars().all())

    async def is_member(self, group_id: int, user_id: int) -> bool:
        """
        Check if a user is a member of a group.

        Args:
            group_id: The group ID to check
            user_id: The user ID to check

        Returns:
            bool: True if user is a member, False otherwise
        """
        result = await self.session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None
