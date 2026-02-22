from pydantic import BaseModel
from typing import List
from app.schemas.building import BuildingResponse
from app.schemas.activity import ActivityResponse

class OrganizationPhoneSchema(BaseModel):
    id: int
    phone: str

    class Config:
        from_attributes = True


class OrganizationCreate(BaseModel):
    name: str
    building_id: int
    phone_numbers: List[str]
    activity_ids: List[int]


class OrganizationResponse(BaseModel):
    id: int
    name: str
    building: BuildingResponse
    phones: List[OrganizationPhoneSchema]
    activities: List[ActivityResponse]

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    id: int
    name: str
    building: BuildingResponse
    phones: List[OrganizationPhoneSchema]
    activities: List[ActivityResponse]

    class Config:
        from_attributes = True
