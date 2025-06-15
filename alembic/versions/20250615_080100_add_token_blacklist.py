"""add token blacklist table"""
from alembic import op
import sqlalchemy as sa

revision = 'add_token_blacklist'
down_revision = 'create_auth_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'token_blacklist',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('jti', sa.String(length=36), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('token_blacklist')
