from sqlalchemy.orm import Session
from app.models import Activity


def get_activity_level(activity: Activity, level: int = 0) -> int:
    if activity.parent_id is None:
        return level
    return get_activity_level(activity.parent, level + 1)


def get_activity_subtree_ids(db: Session, activity_id: int) -> list[int]:
    """Return activity_id and all descendant ids (for search by activity including children)."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return []
    result = [activity.id]
    children = db.query(Activity).filter(Activity.parent_id == activity_id).all()
    for child in children:
        result.extend(get_activity_subtree_ids(db, child.id))
    return result
