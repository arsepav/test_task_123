from math import radians, sin, cos, sqrt, atan2
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Building
from app.schemas.building import BuildingResponse

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("", response_model=list[BuildingResponse])
def list_buildings(
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    radius_km: float | None = Query(None),
    lat_min: float | None = Query(None),
    lat_max: float | None = Query(None),
    lon_min: float | None = Query(None),
    lon_max: float | None = Query(None),
):
    if radius_km is not None and lat is not None and lon is not None:
        R = 6371
        lat_r, lon_r = radians(lat), radians(lon)
        delta = radius_km / 111.0
        buildings = (
            db.query(Building)
            .filter(
                and_(
                    Building.latitude >= lat - delta,
                    Building.latitude <= lat + delta,
                    Building.longitude >= lon - delta,
                    Building.longitude <= lon + delta,
                )
            )
            .all()
        )
        out = []
        for b in buildings:
            dlat = radians(b.latitude) - lat_r
            dlon = radians(b.longitude) - lon_r
            a = sin(dlat / 2) ** 2 + cos(lat_r) * cos(radians(b.latitude)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            if R * c <= radius_km:
                out.append(b)
        return out
    if all(x is not None for x in (lat_min, lat_max, lon_min, lon_max)):
        return (
            db.query(Building)
            .filter(
                and_(
                    Building.latitude >= lat_min,
                    Building.latitude <= lat_max,
                    Building.longitude >= lon_min,
                    Building.longitude <= lon_max,
                )
            )
            .all()
        )
    return db.query(Building).all()
