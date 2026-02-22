from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True)
)


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    phone = Column(String(64), nullable=False)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", backref="organizations")
    phones = relationship("OrganizationPhone", backref="organization", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary=organization_activities, backref="organizations")
