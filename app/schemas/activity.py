from pydantic import BaseModel
from typing import Optional


class ActivityCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True
