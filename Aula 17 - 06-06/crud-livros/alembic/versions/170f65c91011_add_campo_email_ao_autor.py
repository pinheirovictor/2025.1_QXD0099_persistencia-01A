"""add campo email ao autor

Revision ID: 170f65c91011
Revises: 937c3618c079
Create Date: 2025-06-06 11:26:16.234125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '170f65c91011'
down_revision: Union[str, None] = '937c3618c079'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adiciona a coluna 'email' na tabela 'autor'
    op.add_column('autor', sa.Column('email', sa.String(), nullable=True))
    # Cria índice para a coluna 'email'
    op.create_index(op.f('ix_autor_email'), 'autor', ['email'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_autor_email'), table_name='autor')
    op.drop_column('autor', 'email')
