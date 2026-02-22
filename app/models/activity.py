from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children")
