"""add is_social flag to users"""

from alembic import op
import sqlalchemy as sa

revision = "add_is_social"
down_revision = "add_email_confirmation"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("is_social", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade():
    op.drop_column("users", "is_social")
