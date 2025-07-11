"""update barang

Revision ID: f06b92521b1d
Revises: 832612437783
Create Date: 2025-06-30 19:15:20.347671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f06b92521b1d'
down_revision: Union[str, Sequence[str], None] = '832612437783'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('nama', sa.String(), nullable=False),
    sa.Column('telepon', sa.String(), nullable=False),
    sa.Column('alamat', sa.String(), nullable=False),
    sa.Column('id_barang', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id_barang'], ['barang.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_barang')
    )
    op.create_index(op.f('ix_supplier_id'), 'supplier', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_supplier_id'), table_name='supplier')
    op.drop_table('supplier')
    # ### end Alembic commands ###
