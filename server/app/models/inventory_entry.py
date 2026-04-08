from app import db
from datetime import datetime

class InventoryEntry(db.Model):
    __tablename__ = 'inventory_entries'

    id = db.Column(db.Integer, primary_key=True)
    store_product_id = db.Column(db.Integer, db.ForeignKey('store_products.id'), nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity_received = db.Column(db.Integer, default=0)
    quantity_in_stock = db.Column(db.Integer, default=0)
    quantity_spoilt = db.Column(db.Integer, default=0)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='unpaid')
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships - Updated for new junction table
    store_product = db.relationship('StoreProduct', back_populates='inventory_entries')
    clerk = db.relationship('User', back_populates='inventory_entries')