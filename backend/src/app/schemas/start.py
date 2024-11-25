from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.users import GroupSchema, UserSchema


class StartMode(str, Enum):
    DRAW = "draw"


class StartParamsRequest(BaseModel):
    user_token: Optional[str] = None
    group_token: Optional[str] = None
    referal_id: Optional[str] = None
    mode: Optional[StartMode] = None


class StartData(BaseModel):
    current_user: UserSchema
    inviter: Optional[GroupSchema] = None
    mode: Optional[StartMode] = None
