"""Initial schema: buildings, activities, organizations, phones, organization_activities

Revision ID: 001
Revises:
Create Date: 2025-02-20

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(512), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_buildings_id"), "buildings", ["id"], unique=False)

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["activities.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_activities_id"), "activities", ["id"], unique=False)
    op.create_index(op.f("ix_activities_parent_id"), "activities", ["parent_id"], unique=False)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organizations_id"), "organizations", ["id"], unique=False)
    op.create_index(op.f("ix_organizations_building_id"), "organizations", ["building_id"], unique=False)

    op.create_table(
        "organization_phones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organization_phones_id"), "organization_phones", ["id"], unique=False)

    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )


def downgrade() -> None:
    op.drop_table("organization_activities")
    op.drop_index(op.f("ix_organization_phones_id"), table_name="organization_phones")
    op.drop_table("organization_phones")
    op.drop_index(op.f("ix_organizations_building_id"), table_name="organizations")
    op.drop_index(op.f("ix_organizations_id"), table_name="organizations")
    op.drop_table("organizations")
    op.drop_index(op.f("ix_activities_parent_id"), table_name="activities")
    op.drop_index(op.f("ix_activities_id"), table_name="activities")
    op.drop_table("activities")
    op.drop_index(op.f("ix_buildings_id"), table_name="buildings")
    op.drop_table("buildings")
