"""Seed data from JSON

Revision ID: 002
Revises: 001
Create Date: 2025-02-20

"""
from pathlib import Path
import json
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _load_seed_data():
    path = Path(__file__).resolve().parent / "seed_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def upgrade() -> None:
    data = _load_seed_data()
    conn = op.get_bind()

    for row in data["buildings"]:
        conn.execute(
            sa.text(
                "INSERT INTO buildings (id, address, latitude, longitude) VALUES (:id, :address, :latitude, :longitude)"
            ),
            row,
        )

    for row in data["activities"]:
        conn.execute(
            sa.text(
                "INSERT INTO activities (id, name, parent_id) VALUES (:id, :name, :parent_id)"
            ),
            row,
        )

    for row in data["organizations"]:
        conn.execute(
            sa.text(
                "INSERT INTO organizations (id, name, building_id) VALUES (:id, :name, :building_id)"
            ),
            row,
        )

    for row in data["organization_phones"]:
        conn.execute(
            sa.text(
                "INSERT INTO organization_phones (id, organization_id, phone) VALUES (:id, :organization_id, :phone)"
            ),
            row,
        )

    for row in data["organization_activities"]:
        conn.execute(
            sa.text(
                "INSERT INTO organization_activities (organization_id, activity_id) VALUES (:organization_id, :activity_id)"
            ),
            row,
        )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM organization_activities"))
    conn.execute(sa.text("DELETE FROM organization_phones"))
    conn.execute(sa.text("DELETE FROM organizations"))
    conn.execute(sa.text("DELETE FROM activities"))
    conn.execute(sa.text("DELETE FROM buildings"))
