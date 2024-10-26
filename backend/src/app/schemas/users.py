from typing import Optional

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

    model_config = ConfigDict(from_attributes=True)
