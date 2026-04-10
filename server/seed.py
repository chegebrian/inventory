from app import create_app, db
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.inventory_entry import InventoryEntry
from app.models.supply_request import SupplyRequest

import bcrypt
from datetime import datetime, timedelta
import random

app = create_app()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed():
    with app.app_context():

        print("Clearing existing data...")

        SupplyRequest.query.delete()
        InventoryEntry.query.delete()
        Product.query.delete()
        User.query.delete()
        Store.query.delete()
        db.session.commit()

        print("Creating stores...")

        store1 = Store(name="Nairobi CBD Branch", location="Nairobi CBD")
        store2 = Store(name="Westlands Branch", location="Westlands")
        store3 = Store(name="Mombasa Branch", location="Mombasa")

        db.session.add_all([store1, store2, store3])
        db.session.commit()

        print("Creating users...")

        merchant = User(
            full_name="James Mwangi",
            email="merchant@test.com",
            phone_number="0712345678",
            password_hash=hash_password("password123"),
            role="merchant",
            is_active=True,
            is_verified=True,
            store_id=None
        )

        admin1 = User(
            full_name="Admin One",
            email="admin1@test.com",
            phone_number="0723456789",
            password_hash=hash_password("password123"),
            role="admin",
            is_active=True,
            is_verified=True,
            store_id=store1.id
        )

        clerk1 = User(
            full_name="Clerk One",
            email="clerk1@test.com",
            phone_number="0734567890",
            password_hash=hash_password("password123"),
            role="clerk",
            is_active=True,
            is_verified=True,
            store_id=store1.id
        )

        db.session.add_all([merchant, admin1, clerk1])
        db.session.commit()

        print("Creating products...")

        product1 = Product(
            name="Sugar 1kg",
            description="White sugar",
            store_id=store1.id
        )

        db.session.add(product1)
        db.session.commit()

        print("Creating inventory...")

        entry = InventoryEntry(
            product_id=product1.id,
            clerk_id=clerk1.id,
            quantity_received=100,
            quantity_in_stock=90,
            quantity_spoilt=10,
            buying_price=100,
            selling_price=130,
            payment_status="paid",
            recorded_at=datetime.utcnow()
        )

        db.session.add(entry)
        db.session.commit()

        print("Creating supply request...")

        request = SupplyRequest(
            product_id=product1.id,
            clerk_id=clerk1.id,
            store_id=store1.id,
            quantity_requested=50,
            status="pending",
            note="Restock needed",
            created_at=datetime.utcnow()
        )

        db.session.add(request)
        db.session.commit()

        print("\nDatabase seeded successfully!")
        print("Login: merchant@test.com / password123")


if __name__ == "__main__":
    seed()