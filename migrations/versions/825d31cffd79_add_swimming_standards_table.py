"""Add swimming standards table

Revision ID: 825d31cffd79
Revises: 26245a0d8d00
Create Date: 2026-07-12 16:30:39.678671

"""

from alembic import op
import sqlalchemy as sa


revision = '825d31cffd79'
down_revision = '26245a0d8d00'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'swim_standard',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'gender',
            sa.String(length=20),
            nullable=True
        ),

        sa.Column(
            'age',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'event',
            sa.String(length=50),
            nullable=True
        ),

        sa.Column(
            'level',
            sa.String(length=20),
            nullable=True
        ),

        sa.Column(
            'time',
            sa.String(length=20),
            nullable=True
        ),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade():

    op.drop_table('swim_standard')