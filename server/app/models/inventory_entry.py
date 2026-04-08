from app import db
from datetime import datetime

class InventoryEntry(db.Model):
    __tablename__ = 'inventory_entries'