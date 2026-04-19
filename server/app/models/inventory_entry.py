from app import db
from datetime import datetime

class InventoryEntry(db.Model):
    __tablename__ = 'inventory_entries'

    id = db.Column(db.Integer, primary_key=True)

    # 🔥 DIRECT RELATIONSHIP (NO MORE STOREPRODUCT DEPENDENCY)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    quantity_received = db.Column(db.Integer, default=0)
    quantity_in_stock = db.Column(db.Integer, default=0)
    quantity_spoilt = db.Column(db.Integer, default=0)

    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)

    payment_status = db.Column(db.String(20), default='unpaid')
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    store = db.relationship('Store', foreign_keys=[store_id])
    product = db.relationship('Product', foreign_keys=[product_id])
    clerk = db.relationship('User', foreign_keys=[clerk_id])

    def to_dict(self):
        return {
            'id': self.id,
            'store_id': self.store_id,
            'product_id': self.product_id,

            'product_name': self.product.name if self.product else None,
            'store_name': self.store.name if self.store else None,

            'clerk_id': self.clerk_id,
            'clerk_name': self.clerk.full_name if self.clerk else None,

            'quantity_received': self.quantity_received,
            'quantity_in_stock': self.quantity_in_stock,
            'quantity_spoilt': self.quantity_spoilt,

            'buying_price': self.buying_price,
            'selling_price': self.selling_price,
            'payment_status': self.payment_status,

            'recorded_at': (
                self.recorded_at.strftime('%B %d, %Y %I:%M %p')
                if self.recorded_at else None
            )
        }