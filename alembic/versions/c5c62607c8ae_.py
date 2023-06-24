"""empty message

Revision ID: c5c62607c8ae
Revises: 
Create Date: 2023-06-24 14:40:25.853020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c5c62607c8ae"
down_revision = None
branch_labels = None
depends_on = None

"""

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("now()"),
    )
"""


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer()),
        sa.Column("username", sa.String(80), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", "username"),
    )
    pass


def downgrade() -> None:
    op.drop_table("user")
    pass
