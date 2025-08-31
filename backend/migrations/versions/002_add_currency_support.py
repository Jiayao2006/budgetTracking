"""Add currency support to users and spendings

Revision ID: 002_add_currency_support
Revises: 
Create Date: 2025-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_currency_support'
down_revision = None
depends_on = None


def upgrade():
    # Add currency columns to users table
    op.add_column('users', sa.Column('preferred_currency', sa.String(3), nullable=False, server_default='USD'))
    
    # Add currency columns to spendings table
    op.add_column('spendings', sa.Column('original_amount', sa.Float(), nullable=True))
    op.add_column('spendings', sa.Column('original_currency', sa.String(3), nullable=True))
    op.add_column('spendings', sa.Column('display_currency', sa.String(3), nullable=True))
    op.add_column('spendings', sa.Column('exchange_rate', sa.Float(), nullable=True))
    
    # Update existing records to have default values
    op.execute("UPDATE spendings SET original_amount = amount WHERE original_amount IS NULL")
    op.execute("UPDATE spendings SET original_currency = 'USD' WHERE original_currency IS NULL")
    op.execute("UPDATE spendings SET display_currency = 'USD' WHERE display_currency IS NULL")
    op.execute("UPDATE spendings SET exchange_rate = 1.0 WHERE exchange_rate IS NULL")
    
    # Make columns non-nullable after setting default values
    op.alter_column('spendings', 'original_amount', nullable=False)
    op.alter_column('spendings', 'original_currency', nullable=False)
    op.alter_column('spendings', 'display_currency', nullable=False)
    op.alter_column('spendings', 'exchange_rate', nullable=False)


def downgrade():
    # Remove currency columns from spendings table
    op.drop_column('spendings', 'exchange_rate')
    op.drop_column('spendings', 'display_currency')
    op.drop_column('spendings', 'original_currency')
    op.drop_column('spendings', 'original_amount')
    
    # Remove currency column from users table
    op.drop_column('users', 'preferred_currency')
