from pydantic import BaseModel


class BuildingCreate(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

