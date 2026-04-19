"""fresh inventory schema

Revision ID: 8e4ca571d452
Revises: 
Create Date: 2026-04-19 17:09:55.127940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e4ca571d452'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_url', sa.String(length=300), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # ✅ Create users WITHOUT the store_id FK first
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('reset_token', sa.String(length=256), nullable=True),
    sa.Column('reset_token_expiry', sa.DateTime(), nullable=True),
    sa.Column('invite_token', sa.String(length=256), nullable=True),
    sa.Column('invite_token_expiry', sa.DateTime(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )

    # ✅ Create stores (users exists now, so FK works)
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # ✅ Now add the store_id FK to users
    op.create_foreign_key('fk_users_store_id', 'users', 'stores', ['store_id'], ['id'])

    op.create_table('inventory_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('clerk_id', sa.Integer(), nullable=False),
    sa.Column('quantity_received', sa.Integer(), nullable=True),
    sa.Column('quantity_in_stock', sa.Integer(), nullable=True),
    sa.Column('quantity_spoilt', sa.Integer(), nullable=True),
    sa.Column('buying_price', sa.Float(), nullable=False),
    sa.Column('selling_price', sa.Float(), nullable=False),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.Column('recorded_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['clerk_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('store_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('supply_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store_product_id', sa.Integer(), nullable=False),
    sa.Column('clerk_id', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('quantity_requested', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['clerk_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.ForeignKeyConstraint(['store_product_id'], ['store_products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('supply_requests')
    op.drop_table('store_products')
    op.drop_table('inventory_entries')
    # ✅ Drop the FK before dropping tables
    op.drop_constraint('fk_users_store_id', 'users', type_='foreignkey')
    op.drop_table('users')
    op.drop_table('stores')
    op.drop_table('products')