"""adding recipe table

Revision ID: 6b0d6c987194
Revises: c5c62607c8ae
Create Date: 2023-06-24 15:05:36.987299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6b0d6c987194"
down_revision = "c5c62607c8ae"
branch_labels = None
depends_on = None

"""
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200))
    num_of_servings = Column(Integer)
    cook_time = Column(Integer)
    directions = Column(String(1000))
    is_publish = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("now()"),
    )
    user_id = Column(Integer, ForeignKey="user.id")
"""


def upgrade() -> None:
    op.create_table(
        "recipe",
        sa.Column("id", sa.Integer()),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(200)),
        sa.Column("num_of_servings", sa.Integer()),
        sa.Column("cook_time", sa.Integer()),
        sa.Column("directions", sa.String(1000)),
        sa.Column("is_publish", sa.Boolean(), default=False),
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
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            columns=["user_id"], refcolumns=["user.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("recipe")
    pass
