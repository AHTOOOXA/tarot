from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: Optional[bool] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None

    app_username: Optional[str] = None
    app_language_code: Optional[str] = None
    male: Optional[bool] = None
    birth_date: Optional[date] = None
    is_onboarded: Optional[bool] = None
    is_terms_accepted: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GroupSchema(BaseModel):
    group_id: int
    title: str
    users: List[UserSchema]


class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None

    app_username: Optional[str] = None
    app_language_code: Optional[str] = None
    male: Optional[bool] = None
    birth_date: Optional[date] = None
    is_onboarded: Optional[bool] = None
    is_terms_accepted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
