from app import create_app, db
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.store_product import StoreProduct
from app.models.inventory_entry import InventoryEntry
from app.models.supply_request import SupplyRequest

import bcrypt
import random
from datetime import datetime

app = create_app()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed():
    with app.app_context():

        print("Clearing existing data...")

        SupplyRequest.query.delete()
        InventoryEntry.query.delete()
        StoreProduct.query.delete()
        Product.query.delete()
        User.query.delete()
        Store.query.delete()
        db.session.commit()

        # =====================================
        # 1. CREATE MERCHANT
        # =====================================
        print("Creating merchant...")

        merchant = User(
            full_name="James Mwangi",
            email="merchant@test.com",
            phone_number="0712345678",
            password_hash=hash_password("password123"),
            role="merchant",
            is_active=True,
            is_verified=True
        )

        db.session.add(merchant)
        db.session.commit()

        # =====================================
        # 2. CREATE STORES
        # =====================================
        print("Creating stores...")

        store1 = Store(name="Nairobi CBD Branch", location="Nairobi CBD", merchant_id=merchant.id)
        store2 = Store(name="Westlands Branch", location="Westlands", merchant_id=merchant.id)
        store3 = Store(name="Mombasa Branch", location="Mombasa", merchant_id=merchant.id)

        db.session.add_all([store1, store2, store3])
        db.session.commit()

        # =====================================
        # 3. CREATE USERS
        # =====================================
        print("Creating users...")

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

        customer = User(
            full_name="John Customer",
            email="customer@test.com",
            phone_number="0745678901",
            password_hash=hash_password("password123"),
            role="customer",
            is_active=True,
            is_verified=True
        )

        db.session.add_all([admin1, clerk1, customer])
        db.session.commit()

        # =====================================
        # 4. CREATE PRODUCTS (REALISTIC)
        # =====================================
        print("Creating products...")

        products = [
            Product(name="Sugar 1kg", description="White sugar"),
            Product(name="Maize Flour 2kg", description="Unga wa ugali"),
            Product(name="Rice 1kg", description="Pishori rice"),
            Product(name="Beans 1kg", description="Red beans"),
            Product(name="Cooking Oil 1L", description="Vegetable oil"),
            Product(name="Milk 500ml", description="Fresh milk"),
            Product(name="Milk 1L", description="Long life milk"),
            Product(name="Butter 250g", description="Salted butter"),
            Product(name="Yogurt 500ml", description="Vanilla yogurt"),
            Product(name="Bread White", description="White bread loaf"),
            Product(name="Bread Brown", description="Brown bread loaf"),
            Product(name="Mandazi", description="Fried dough snack"),
            Product(name="Coca Cola 500ml", description="Soft drink"),
            Product(name="Fanta 500ml", description="Orange soda"),
            Product(name="Sprite 500ml", description="Lemon soda"),
            Product(name="Mineral Water 1L", description="Drinking water"),
            Product(name="Soap Bar", description="Laundry soap"),
            Product(name="Detergent 1kg", description="Washing powder"),
            Product(name="Toothpaste", description="Colgate"),
            Product(name="Toilet Paper", description="2 ply tissue"),
            Product(name="Biscuits", description="Assorted biscuits"),
            Product(name="Crisps", description="Potato chips"),
            Product(name="Chocolate Bar", description="Sweet chocolate"),
            Product(name="Shampoo", description="Hair shampoo"),
            Product(name="Body Lotion", description="Skin lotion"),
            Product(name="Deodorant", description="Body spray"),
        ]

        db.session.add_all(products)
        db.session.commit()

        # =====================================
        # 5. LINK PRODUCTS TO STORES
        # =====================================
        print("Linking products to stores...")

        store_products = []

        for store in [store1, store2, store3]:
            for product in products:
                store_products.append(
                    StoreProduct(
                        store_id=store.id,
                        product_id=product.id
                    )
                )

        db.session.add_all(store_products)
        db.session.commit()

        # =====================================
        # 6. CREATE INVENTORY (REALISTIC)
        # =====================================
        print("Creating inventory...")

        entries = []

        for sp in store_products:
            entries.append(
                InventoryEntry(
                    store_product_id=sp.id,
                    clerk_id=clerk1.id,
                    quantity_received=random.randint(50, 300),
                    quantity_in_stock=random.randint(20, 250),
                    quantity_spoilt=random.randint(0, 30),
                    buying_price=random.randint(50, 200),
                    selling_price=random.randint(80, 350),
                    payment_status=random.choice(["paid", "pending"]),
                    recorded_at=datetime.utcnow()
                )
            )

        db.session.add_all(entries)
        db.session.commit()

        # =====================================
        # 7. CREATE SUPPLY REQUESTS
        # =====================================
        print("Creating supply requests...")

        requests = []

        for sp in store_products[:15]:
            requests.append(
                SupplyRequest(
                    store_product_id=sp.id,
                    clerk_id=clerk1.id,
                    store_id=store1.id,
                    quantity_requested=random.randint(20, 100),
                    status=random.choice(["pending", "approved"]),
                    note="Restock needed",
                    created_at=datetime.utcnow()
                )
            )

        db.session.add_all(requests)
        db.session.commit()

        print("\n✅ Database seeded successfully!")
        print("👉 Merchant: merchant@test.com / password123")
        print("👉 Admin: admin1@test.com / password123")
        print("👉 Clerk: clerk1@test.com / password123")
        print("👉 Customer: customer@test.com / password123")


if __name__ == "__main__":
    seed()