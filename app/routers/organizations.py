from math import radians, sin, cos, sqrt, atan2
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Organization, Building, Activity
from app.schemas.organization import OrganizationResponse, OrganizationListResponse
from app.services.activity import get_activity_subtree_ids

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/building/{building_id}", response_model=list[OrganizationListResponse])
def list_organizations_by_building(building_id: int, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    return db.query(Organization).filter(Organization.building_id == building_id).all()


@router.get("/activity/{activity_id}", response_model=list[OrganizationListResponse])
def list_organizations_by_activity(activity_id: int, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    return (
        db.query(Organization)
        .join(Organization.activities)
        .filter(Organization.activities.any(id=activity_id))
        .distinct()
        .all()
    )


@router.get("/nearby", response_model=list[OrganizationListResponse])
def list_organizations_nearby(
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
        ids = []
        for b in buildings:
            dlat = radians(b.latitude) - lat_r
            dlon = radians(b.longitude) - lon_r
            a = sin(dlat / 2) ** 2 + cos(lat_r) * cos(radians(b.latitude)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            if R * c <= radius_km:
                ids.append(b.id)
        return db.query(Organization).filter(Organization.building_id.in_(ids)).all()
    if all(x is not None for x in (lat_min, lat_max, lon_min, lon_max)):
        buildings = (
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
        ids = [b.id for b in buildings]
        return db.query(Organization).filter(Organization.building_id.in_(ids)).all()
    raise HTTPException(400, detail="Укажите (lat, lon, radius_km) или (lat_min, lat_max, lon_min, lon_max)")


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(organization_id: int, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(404, detail="Organization not found")
    return org


@router.get("/search/activity", response_model=list[OrganizationListResponse])
def search_organizations_by_activity(
    activity_id: int = Query(...), db: Session = Depends(get_db), _: str = Depends(verify_api_key)
):
    ids = get_activity_subtree_ids(db, activity_id)
    if not ids:
        return []
    return (
        db.query(Organization)
        .join(Organization.activities)
        .filter(Activity.id.in_(ids))
        .distinct()
        .all()
    )


@router.get("/search/name", response_model=list[OrganizationListResponse])
def search_organizations_by_name(q: str = Query(..., min_length=1), db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    return db.query(Organization).filter(Organization.name.ilike(f"%{q}%")).all()
