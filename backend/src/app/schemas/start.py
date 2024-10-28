from typing import Optional

from pydantic import BaseModel

from app.schemas.users import GroupSchema, UserSchema


class StartParams(BaseModel):
    user_token: str
    group_token: str
    referal_id: str


class StartData(BaseModel):
    current_user: UserSchema
    inviter: Optional[UserSchema | GroupSchema]
