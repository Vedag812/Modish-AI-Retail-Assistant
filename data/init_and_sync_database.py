"""
Database Initialization and Sync Script
Creates comprehensive product catalog for both PostgreSQL AND SQLite
"""
import psycopg2
import sqlite3
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Database configuration
POSTGRES_URL = os.getenv("DATABASE_URL")
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "retail_sales.db")

# Extended product catalog with 50+ products
PRODUCTS = [
    # Electronics
    {"sku": "ELEC1001", "name": "iPhone 15 Pro", "category": "Electronics", "price": 999.99, "rating": 4.8, "reviews": 2340},
    {"sku": "ELEC1002", "name": "Samsung Galaxy S24", "category": "Electronics", "price": 899.99, "rating": 4.7, "reviews": 1890},
    {"sku": "ELEC1003", "name": "MacBook Pro 14-inch", "category": "Electronics", "price": 1999.99, "rating": 4.9, "reviews": 3210},
    {"sku": "ELEC1004", "name": "Dell XPS 15", "category": "Electronics", "price": 1599.99, "rating": 4.6, "reviews": 1456},
    {"sku": "ELEC1005", "name": "iPad Air", "category": "Electronics", "price": 599.99, "rating": 4.7, "reviews": 987},
    {"sku": "ELEC1006", "name": "Sony WH-1000XM5 Headphones", "category": "Electronics", "price": 399.99, "rating": 4.9, "reviews": 2567},
    {"sku": "ELEC1007", "name": "Bose QuietComfort 45", "category": "Electronics", "price": 329.99, "rating": 4.8, "reviews": 1234},
    {"sku": "ELEC1008", "name": "Apple Watch Series 9", "category": "Electronics", "price": 429.99, "rating": 4.7, "reviews": 1678},
    {"sku": "ELEC1009", "name": "Kindle Paperwhite", "category": "Electronics", "price": 139.99, "rating": 4.6, "reviews": 5432},
    {"sku": "ELEC1010", "name": "GoPro HERO 12", "category": "Electronics", "price": 449.99, "rating": 4.8, "reviews": 890},
    
    # Sports & Outdoors
    {"sku": "SPORT1001", "name": "Nike Air Zoom Pegasus 40", "category": "Sports & Outdoors", "price": 129.99, "rating": 4.7, "reviews": 1234},
    {"sku": "SPORT1002", "name": "Adidas Ultraboost 23", "category": "Sports & Outdoors", "price": 189.99, "rating": 4.8, "reviews": 987},
    {"sku": "SPORT1003", "name": "New Balance 990v6", "category": "Sports & Outdoors", "price": 199.99, "rating": 4.9, "reviews": 765},
    {"sku": "SPORT1004", "name": "ASICS Gel-Kayano 30", "category": "Sports & Outdoors", "price": 159.99, "rating": 4.6, "reviews": 543},
    {"sku": "SPORT1005", "name": "Brooks Ghost 15", "category": "Sports & Outdoors", "price": 139.99, "rating": 4.7, "reviews": 876},
    {"sku": "SPORT1006", "name": "Yoga Mat Premium", "category": "Sports & Outdoors", "price": 29.99, "rating": 4.5, "reviews": 534},
    {"sku": "SPORT1007", "name": "Dumbbell Set 20lb", "category": "Sports & Outdoors", "price": 89.99, "rating": 4.6, "reviews": 432},
    {"sku": "SPORT1008", "name": "Resistance Bands Set", "category": "Sports & Outdoors", "price": 24.99, "rating": 4.4, "reviews": 678},
    {"sku": "SPORT1009", "name": "Camping Tent 4-Person", "category": "Sports & Outdoors", "price": 139.99, "rating": 4.7, "reviews": 234},
    {"sku": "SPORT1010", "name": "Fitness Tracker", "category": "Sports & Outdoors", "price": 44.99, "rating": 4.3, "reviews": 678},
    {"sku": "SPORT1011", "name": "Basketball Wilson Evolution", "category": "Sports & Outdoors", "price": 64.99, "rating": 4.9, "reviews": 1567},
    {"sku": "SPORT1012", "name": "Soccer Ball Adidas", "category": "Sports & Outdoors", "price": 49.99, "rating": 4.6, "reviews": 890},
    
    # Clothing
    {"sku": "CLOTH1001", "name": "Nike Dri-FIT T-Shirt", "category": "Clothing", "price": 34.99, "rating": 4.5, "reviews": 890},
    {"sku": "CLOTH1002", "name": "Levi's 501 Jeans", "category": "Clothing", "price": 79.99, "rating": 4.7, "reviews": 1234},
    {"sku": "CLOTH1003", "name": "North Face Jacket", "category": "Clothing", "price": 199.99, "rating": 4.8, "reviews": 765},
    {"sku": "CLOTH1004", "name": "Adidas Track Pants", "category": "Clothing", "price": 54.99, "rating": 4.6, "reviews": 543},
    {"sku": "CLOTH1005", "name": "Under Armour Hoodie", "category": "Clothing", "price": 64.99, "rating": 4.7, "reviews": 678},
    {"sku": "CLOTH1006", "name": "Columbia Fleece", "category": "Clothing", "price": 89.99, "rating": 4.6, "reviews": 432},
    
    # Home & Kitchen
    {"sku": "HOME1001", "name": "Ninja Air Fryer", "category": "Home & Kitchen", "price": 129.99, "rating": 4.8, "reviews": 3456},
    {"sku": "HOME1002", "name": "Instant Pot Duo 7-in-1", "category": "Home & Kitchen", "price": 99.99, "rating": 4.7, "reviews": 5678},
    {"sku": "HOME1003", "name": "Keurig K-Elite Coffee Maker", "category": "Home & Kitchen", "price": 159.99, "rating": 4.6, "reviews": 2345},
    {"sku": "HOME1004", "name": "Dyson V11 Vacuum", "category": "Home & Kitchen", "price": 599.99, "rating": 4.9, "reviews": 1234},
    {"sku": "HOME1005", "name": "iRobot Roomba j7+", "category": "Home & Kitchen", "price": 799.99, "rating": 4.8, "reviews": 987},
    {"sku": "HOME1006", "name": "Cuisinart Food Processor", "category": "Home & Kitchen", "price": 149.99, "rating": 4.7, "reviews": 765},
    
    # Beauty & Personal Care
    {"sku": "BEAUTY1001", "name": "Dyson Airwrap", "category": "Beauty & Personal Care", "price": 549.99, "rating": 4.9, "reviews": 1234},
    {"sku": "BEAUTY1002", "name": "Oral-B Electric Toothbrush", "category": "Beauty & Personal Care", "price": 89.99, "rating": 4.7, "reviews": 2345},
    {"sku": "BEAUTY1003", "name": "Philips Norelco Shaver", "category": "Beauty & Personal Care", "price": 179.99, "rating": 4.6, "reviews": 876},
    {"sku": "BEAUTY1004", "name": "Revlon Hair Dryer", "category": "Beauty & Personal Care", "price": 59.99, "rating": 4.5, "reviews": 1567},
    
    # Books & Media
    {"sku": "BOOK1001", "name": "Atomic Habits - James Clear", "category": "Books", "price": 16.99, "rating": 4.9, "reviews": 15678},
    {"sku": "BOOK1002", "name": "The Subtle Art of Not Giving", "category": "Books", "price": 14.99, "rating": 4.6, "reviews": 12345},
    {"sku": "BOOK1003", "name": "Sapiens - Yuval Noah Harari", "category": "Books", "price": 18.99, "rating": 4.8, "reviews": 23456},
    
    # Toys & Games
    {"sku": "TOY1001", "name": "LEGO Star Wars Millennium Falcon", "category": "Toys & Games", "price": 179.99, "rating": 4.9, "reviews": 2345},
    {"sku": "TOY1002", "name": "Nintendo Switch OLED", "category": "Toys & Games", "price": 349.99, "rating": 4.8, "reviews": 3456},
    {"sku": "TOY1003", "name": "PlayStation 5", "category": "Toys & Games", "price": 499.99, "rating": 4.9, "reviews": 5678},
    {"sku": "TOY1004", "name": "Xbox Series X", "category": "Toys & Games", "price": 499.99, "rating": 4.8, "reviews": 4321},
    
    # Automotive
    {"sku": "AUTO1001", "name": "Michelin Wiper Blades", "category": "Automotive", "price": 29.99, "rating": 4.7, "reviews": 890},
    {"sku": "AUTO1002", "name": "Armor All Car Wash Kit", "category": "Automotive", "price": 44.99, "rating": 4.5, "reviews": 543},
    {"sku": "AUTO1003", "name": "Garmin Dash Cam", "category": "Automotive", "price": 199.99, "rating": 4.8, "reviews": 765},
]

# Extended customer data (without age and gender - matching Neon schema)
CUSTOMERS = [
    {
        "customer_id": "CUST1001", "name": "Aarav Sharma", "email": "aarav.sharma@gmail.com",
        "phone": "+91-9876543210", "location": "Mumbai, Maharashtra",
        "loyalty_tier": "Platinum", "loyalty_points": 3500,
        "browsing_history": ["ELEC1001", "SPORT1001", "CLOTH1001"],
        "purchase_history": [{"sku": "ELEC1006", "amount": 399.99, "date": "2025-11-15"}],
        "preferences": {"favorite_categories": ["Electronics", "Sports & Outdoors"], "budget": "premium"}
    },
    {
        "customer_id": "CUST1002", "name": "Priya Patel", "email": "priya.patel@gmail.com",
        "phone": "+91-9876543211", "location": "Ahmedabad, Gujarat",
        "loyalty_tier": "Gold", "loyalty_points": 1800,
        "browsing_history": ["TOY1003", "ELEC1003", "AUTO1003"],
        "purchase_history": [{"sku": "TOY1002", "amount": 349.99, "date": "2025-11-20"}],
        "preferences": {"favorite_categories": ["Toys & Games", "Electronics"], "budget": "high"}
    },
    {
        "customer_id": "CUST1003", "name": "Vikram Singh", "email": "vikram.singh@gmail.com",
        "phone": "+91-9876543212", "location": "Delhi, NCR",
        "loyalty_tier": "Silver", "loyalty_points": 945,
        "browsing_history": ["BEAUTY1001", "CLOTH1003", "BOOK1001"],
        "purchase_history": [{"sku": "BEAUTY1002", "amount": 89.99, "date": "2025-11-25"}],
        "preferences": {"favorite_categories": ["Beauty & Personal Care", "Clothing"], "budget": "moderate"}
    },
    {
        "customer_id": "CUST1004", "name": "Anita Desai", "email": "anita.desai@gmail.com",
        "phone": "+91-9876543213", "location": "Bangalore, Karnataka",
        "loyalty_tier": "Platinum", "loyalty_points": 4250,
        "browsing_history": ["HOME1004", "HOME1005", "AUTO1003"],
        "purchase_history": [{"sku": "HOME1002", "amount": 99.99, "date": "2025-11-18"}],
        "preferences": {"favorite_categories": ["Home & Kitchen", "Automotive"], "budget": "premium"}
    },
    {
        "customer_id": "CUST1005", "name": "Rajesh Kumar", "email": "rajesh.kumar@gmail.com",
        "phone": "+91-9876543214", "location": "Chennai, Tamil Nadu",
        "loyalty_tier": "Gold", "loyalty_points": 2100,
        "browsing_history": ["SPORT1001", "SPORT1002", "CLOTH1001"],
        "purchase_history": [{"sku": "SPORT1006", "amount": 29.99, "date": "2025-11-22"}],
        "preferences": {"favorite_categories": ["Sports & Outdoors", "Clothing"], "budget": "moderate"}
    },
]

def create_postgres_tables(conn):
    """Create all necessary tables in PostgreSQL"""
    cursor = conn.cursor()
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            current_price DECIMAL(10, 2) NOT NULL,
            rating DECIMAL(3, 2) DEFAULT 0,
            reviews_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Customers table (without age/gender - matching Neon schema)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            location TEXT,
            loyalty_tier TEXT DEFAULT 'Bronze',
            loyalty_points INTEGER DEFAULT 0,
            browsing_history TEXT DEFAULT '[]',
            purchase_history TEXT DEFAULT '[]',
            preferences TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT,
            location TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (sku, location),
            FOREIGN KEY (sku) REFERENCES products(sku) ON DELETE CASCADE
        )
    """)
    
    # Promotions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            promo_code TEXT PRIMARY KEY,
            description TEXT,
            discount_percent DECIMAL(5, 2),
            discount_amount DECIMAL(10, 2),
            min_purchase DECIMAL(10, 2),
            valid_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ PostgreSQL tables created")

def insert_data(conn):
    """Insert products, customers, inventory, and promotions into Neon PostgreSQL"""
    cursor = conn.cursor()
    
    # Insert products
    for product in PRODUCTS:
        cursor.execute("""
            INSERT INTO products (sku, name, category, current_price, rating, reviews_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (sku) DO UPDATE SET
                current_price = EXCLUDED.current_price,
                rating = EXCLUDED.rating,
                reviews_count = EXCLUDED.reviews_count
        """, (product["sku"], product["name"], product["category"], product["price"], product["rating"], product["reviews"]))
    
    print(f"✅ Inserted {len(PRODUCTS)} products")
    
    # Insert customers (without age/gender - matching Neon schema)
    for customer in CUSTOMERS:
        cursor.execute("""
            INSERT INTO customers (customer_id, name, email, phone, location,
                                  loyalty_tier, loyalty_points, browsing_history, 
                                  purchase_history, preferences)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO UPDATE SET
                loyalty_points = EXCLUDED.loyalty_points,
                browsing_history = EXCLUDED.browsing_history,
                purchase_history = EXCLUDED.purchase_history
        """, (customer["customer_id"], customer["name"], customer["email"], customer["phone"],
              customer["location"], customer["loyalty_tier"],
              customer["loyalty_points"], json.dumps(customer["browsing_history"]),
              json.dumps(customer["purchase_history"]), json.dumps(customer["preferences"])))
    
    print(f"✅ Inserted {len(CUSTOMERS)} customers")
    
    # Add inventory for products
    locations = ["Online Warehouse", "New York - 5th Avenue", "Los Angeles - Beverly Hills", "Chicago - Michigan Ave"]
    for product in PRODUCTS:
        for location in locations:
            quantity = 100 if location == "Online Warehouse" else 25
            cursor.execute("""
                INSERT INTO inventory (sku, location, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (sku, location) DO UPDATE SET quantity = EXCLUDED.quantity
            """, (product["sku"], location, quantity))
    
    print(f"✅ Added inventory for all products across {len(locations)} locations")
    
    # Add promotions
    promotions = [
        ("WELCOME10", "New customer discount", 10.0, None, 0, (datetime.now() + timedelta(days=30)).isoformat()),
        ("SAVE20", "Save $20 on orders over $100", None, 20.0, 100, (datetime.now() + timedelta(days=30)).isoformat()),
        ("FREESHIP", "Free shipping on orders over $50", None, 0.0, 50, (datetime.now() + timedelta(days=30)).isoformat()),
        ("MEGA30", "30% off electronics", 30.0, None, 200, (datetime.now() + timedelta(days=15)).isoformat()),
    ]
    
    for promo in promotions:
        cursor.execute("""
            INSERT INTO promotions (promo_code, description, discount_percent, discount_amount, min_purchase, valid_until)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (promo_code) DO UPDATE SET
                discount_percent = EXCLUDED.discount_percent,
                valid_until = EXCLUDED.valid_until
        """, promo)
    
    print(f"✅ Added {len(promotions)} promotions")
    
    conn.commit()

def clear_existing_data(conn):
    """Clear all existing data from tables (respecting foreign key constraints)"""
    cursor = conn.cursor()
    print("🗑️  Clearing existing data...")
    
    try:
        # Delete in correct order to respect foreign key constraints
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM promotions")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("✅ Existing data cleared")
    except Exception as e:
        print(f"⚠️  Warning while clearing data: {e}")
        conn.rollback()

def main():
    """Main function to initialize and sync databases"""
    print("\n🚀 Starting Database Initialization and Sync...\n")
    
    # PostgreSQL setup
    if POSTGRES_URL:
        print("☁️  Setting up Neon PostgreSQL database...")
        try:
            pg_conn = psycopg2.connect(POSTGRES_URL)
            create_postgres_tables(pg_conn)
            clear_existing_data(pg_conn)
            insert_data(pg_conn)
            pg_conn.close()
            print("✅ Neon PostgreSQL database synced\n")
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                print(f"❌ PostgreSQL Error: Password authentication failed")
                print("   → Go to https://console.neon.tech to get the correct connection string")
                print("   → Update DATABASE_URL in .env file")
            else:
                print(f"❌ PostgreSQL Error: {e}")
        except Exception as e:
            print(f"❌ PostgreSQL Error: {e}")
    else:
        print("⚠️  No DATABASE_URL found - skipping PostgreSQL setup")
    
    # SQLite setup (for local tools)
    print("💾 Setting up local SQLite database...")
    try:
        sqlite_conn = sqlite3.connect(SQLITE_PATH)
        create_sqlite_tables(sqlite_conn)
        clear_sqlite_data(sqlite_conn)
        insert_sqlite_data(sqlite_conn)
        sqlite_conn.close()
        print("✅ Local SQLite database synced\n")
    except Exception as e:
        print(f"❌ SQLite Error: {e}")
    
    print("🎉 Database initialization complete!")
    print(f"   📊 Products: {len(PRODUCTS)}")
    print(f"   👥 Customers: {len(CUSTOMERS)}")
    print(f"   🏪 Inventory locations: 4")
    print(f"   🎁 Promotions: 4\n")


def create_sqlite_tables(conn):
    """Create all necessary tables in SQLite"""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            current_price REAL NOT NULL,
            rating REAL DEFAULT 0,
            reviews_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            location TEXT,
            loyalty_tier TEXT DEFAULT 'Bronze',
            loyalty_points INTEGER DEFAULT 0,
            browsing_history TEXT,
            purchase_history TEXT,
            preferences TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            location TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES products(sku),
            UNIQUE(sku, location)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            promo_code TEXT PRIMARY KEY,
            description TEXT,
            discount_type TEXT,
            discount_value REAL,
            min_purchase REAL DEFAULT 0,
            valid_until TEXT,
            usage_limit INTEGER DEFAULT -1,
            times_used INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    print("✅ SQLite tables created")


def clear_sqlite_data(conn):
    """Clear existing SQLite data"""
    cursor = conn.cursor()
    print("🗑️  Clearing SQLite data...")
    cursor.execute("DELETE FROM inventory")
    cursor.execute("DELETE FROM promotions")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM products")
    conn.commit()
    print("✅ SQLite data cleared")


def insert_sqlite_data(conn):
    """Insert data into SQLite"""
    cursor = conn.cursor()
    
    # Insert products
    for p in PRODUCTS:
        cursor.execute("""
            INSERT OR REPLACE INTO products (sku, name, category, current_price, rating, reviews_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (p["sku"], p["name"], p["category"], p["price"], p["rating"], p["reviews"]))
    print(f"✅ Inserted {len(PRODUCTS)} products into SQLite")
    
    # Insert customers (without age/gender - matching Neon schema)
    for c in CUSTOMERS:
        cursor.execute("""
            INSERT OR REPLACE INTO customers 
            (customer_id, name, email, phone, location, loyalty_tier, loyalty_points, browsing_history, purchase_history, preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["customer_id"], c["name"], c["email"], c["phone"], c["location"],
            c["loyalty_tier"], c["loyalty_points"],
            json.dumps(c["browsing_history"]), json.dumps(c["purchase_history"]), json.dumps(c["preferences"])
        ))
    print(f"✅ Inserted {len(CUSTOMERS)} customers into SQLite")
    
    # Insert inventory
    locations = ["Chicago - Michigan Ave", "New York - Manhattan", "Los Angeles - Beverly Hills", "San Francisco - Union Square"]
    for p in PRODUCTS:
        for loc in locations:
            cursor.execute("""
                INSERT OR REPLACE INTO inventory (sku, location, quantity)
                VALUES (?, ?, ?)
            """, (p["sku"], loc, 25))
    print(f"✅ Added inventory for all products across {len(locations)} locations")
    
    # Insert promotions
    promotions = [
        ("WELCOME10", "10% off for new customers", "percentage", 10.0, 0.0, "2025-12-31"),
        ("SUMMER25", "Summer sale - 25% off", "percentage", 25.0, 100.0, "2025-12-31"),
        ("FLAT50", "Flat $50 off on orders $200+", "fixed", 50.0, 200.0, "2025-12-31"),
        ("FREESHIP", "Free shipping on orders $75+", "shipping", 0.0, 75.0, "2025-12-31"),
    ]
    for promo in promotions:
        cursor.execute("""
            INSERT OR REPLACE INTO promotions (promo_code, description, discount_type, discount_value, min_purchase, valid_until)
            VALUES (?, ?, ?, ?, ?, ?)
        """, promo)
    print(f"✅ Added {len(promotions)} promotions to SQLite")
    
    conn.commit()

if __name__ == "__main__":
    main()
