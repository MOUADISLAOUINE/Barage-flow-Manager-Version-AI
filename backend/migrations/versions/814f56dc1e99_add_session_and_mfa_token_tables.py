"""add_session_and_mfa_token_tables

Revision ID: 814f56dc1e99
Revises: e41a5e35523b
Create Date: 2026-03-14 16:01:06.558785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '814f56dc1e99'
down_revision: Union[str, None] = 'e41a5e35523b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -- New tables: session & mfa_token --
    op.create_table('mfa_token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id_utilisateur'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mfa_token_id'), 'mfa_token', ['id'], unique=False)
    op.create_index(op.f('ix_mfa_token_user_id'), 'mfa_token', ['user_id'], unique=False)

    op.create_table('session',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('jwt_jti', sa.String(length=200), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id_utilisateur'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_id'), 'session', ['id'], unique=False)
    op.create_index(op.f('ix_session_jwt_jti'), 'session', ['jwt_jti'], unique=True)
    op.create_index(op.f('ix_session_user_id'), 'session', ['user_id'], unique=False)

    # -- Add role index to utilisateur --
    op.create_index(op.f('ix_utilisateur_role'), 'utilisateur', ['role'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_utilisateur_role'), table_name='utilisateur')
    op.drop_index(op.f('ix_session_user_id'), table_name='session')
    op.drop_index(op.f('ix_session_jwt_jti'), table_name='session')
    op.drop_index(op.f('ix_session_id'), table_name='session')
    op.drop_table('session')
    op.drop_index(op.f('ix_mfa_token_user_id'), table_name='mfa_token')
    op.drop_index(op.f('ix_mfa_token_id'), table_name='mfa_token')
    op.drop_table('mfa_token')
