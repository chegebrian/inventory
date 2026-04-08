from app import db
from datetime import datetime

class InventoryEntry(db.Model):
    __tablename__ = 'inventory_entries'

    id = db.Column(db.Integer, primary_key=True)
    store_product_id = db.Column(db.Integer, db.ForeignKey('store_products.id'), nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)