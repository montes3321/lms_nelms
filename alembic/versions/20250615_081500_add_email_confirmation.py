"""add email confirmation fields"""
from alembic import op
import sqlalchemy as sa

revision = 'add_email_confirmation'
down_revision = 'add_token_blacklist'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('email_confirmation_token', sa.String(length=36), unique=True))
    op.alter_column('users', 'is_active', server_default=sa.sql.expression.false())


def downgrade():
    op.alter_column('users', 'is_active', server_default=sa.sql.expression.true())
    op.drop_column('users', 'email_confirmation_token')
