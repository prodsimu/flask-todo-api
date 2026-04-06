from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddMemberBody(BaseModel):
    username: str
    role: Optional[str] = "viewer"


class UpdateMemberRoleBody(BaseModel):
    role: str


class MemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    role: str
    joined_at: datetime

    model_config = {"from_attributes": True}
