"""add_missing_spending_columns

Revision ID: 003
Revises: 002_add_currency_support
Create Date: 2025-08-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_add_currency_support'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to spendings table
    op.add_column('spendings', sa.Column('original_amount', sa.Float(), nullable=True))
    op.add_column('spendings', sa.Column('label', sa.String(100), nullable=True))
    
    # Update original_amount to match amount for existing records
    op.execute("UPDATE spendings SET original_amount = amount WHERE original_amount IS NULL")
    
    # Make original_amount not nullable after setting values
    op.alter_column('spendings', 'original_amount', nullable=False)


def downgrade():
    # Remove columns
    op.drop_column('spendings', 'original_amount')
    op.drop_column('spendings', 'label')
