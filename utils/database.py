"""
Database initialization and management for Retail Sales Agent System
Creates and populates synthetic data for testing
"""
import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.config import DB_PATH, STORE_LOCATIONS, LOYALTY_TIERS

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def create_database():
    """Create all necessary database tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Customer Profiles Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE,
            name TEXT,
            email TEXT,
            phone TEXT,
            loyalty_tier TEXT,
            loyalty_points INTEGER,
            preferred_channel TEXT,
            location TEXT,
            purchase_history TEXT,
            browsing_history TEXT,
            preferences TEXT,
            created_at TEXT
        )
    """)
    
    # Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            name TEXT,
            category TEXT,
            description TEXT,
            base_price REAL,
            current_price REAL,
            attributes TEXT,
            image_url TEXT,
            rating REAL,
            reviews_count INTEGER
        )
    """)
    
    # Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT,
            location TEXT,
            stock_quantity INTEGER,
            reserved_quantity INTEGER,
            last_updated TEXT,
            FOREIGN KEY (sku) REFERENCES products(sku)
        )
    """)
    
    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE,
            customer_id TEXT,
            items TEXT,
            subtotal REAL,
            discount REAL,
            tax REAL,
            total REAL,
            payment_method TEXT,
            payment_status TEXT,
            fulfillment_type TEXT,
            fulfillment_status TEXT,
            store_location TEXT,
            created_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Promotions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            promo_code TEXT UNIQUE,
            description TEXT,
            discount_type TEXT,
            discount_value REAL,
            min_purchase REAL,
            valid_from TEXT,
            valid_until TEXT,
            usage_limit INTEGER,
            times_used INTEGER
        )
    """)
    
    # Session Context Table (for omnichannel continuity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            customer_id TEXT,
            channel TEXT,
            context_data TEXT,
            cart_items TEXT,
            last_updated TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database tables created successfully")

def seed_customers(count=10):
    """Generate synthetic customer profiles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William"]
    last_names = ["Smith", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas"]
    
    channels = ["web_chat", "mobile_app", "whatsapp", "in_store_kiosk"]
    
    for i in range(count):
        customer_id = f"CUST{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.lower().replace(' ', '.')}@email.com"
        phone = f"+1-555-{random.randint(1000, 9999)}"
        
        points = random.randint(0, 5000)
        tier = "bronze"
        for tier_name, tier_data in sorted(LOYALTY_TIERS.items(), key=lambda x: x[1]['min_points'], reverse=True):
            if points >= tier_data['min_points']:
                tier = tier_name
                break
        
        purchase_history = json.dumps([
            {"sku": f"SKU{random.randint(1, 50)}", "date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(), "amount": round(random.uniform(20, 500), 2)}
            for _ in range(random.randint(2, 10))
        ])
        
        browsing_history = json.dumps([
            f"SKU{random.randint(1, 50)}" for _ in range(random.randint(5, 20))
        ])
        
        preferences = json.dumps({
            "favorite_categories": random.sample(["Electronics", "Clothing", "Home & Kitchen", "Sports & Outdoors"], k=2),
            "price_range": random.choice(["budget", "mid-range", "premium"]),
            "notification_preferences": random.choice([True, False])
        })
        
        cursor.execute("""
            INSERT INTO customers (customer_id, name, email, phone, loyalty_tier, loyalty_points,
                                 preferred_channel, location, purchase_history, browsing_history, 
                                 preferences, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer_id, name, email, phone, tier, points, random.choice(channels),
              random.choice(STORE_LOCATIONS), purchase_history, browsing_history, 
              preferences, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} customer profiles")

def seed_products():
    """Generate synthetic product catalog"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    products = [
        # Electronics
        ("SKU1001", "Wireless Bluetooth Headphones", "Electronics", "Premium noise-canceling headphones with 30-hour battery", 149.99, 129.99, '{"color": "black", "brand": "TechSound", "warranty": "2 years"}', 4.5, 234),
        ("SKU1002", "4K Smart TV 55 inch", "Electronics", "Ultra HD Smart TV with HDR and streaming apps", 599.99, 549.99, '{"size": "55 inch", "resolution": "4K", "smart": true}', 4.7, 567),
        ("SKU1003", "Laptop 15.6 inch", "Electronics", "Powerful laptop with Intel i7, 16GB RAM, 512GB SSD", 899.99, 849.99, '{"processor": "i7", "ram": "16GB", "storage": "512GB SSD"}', 4.6, 432),
        ("SKU1004", "Smartphone 128GB", "Electronics", "Latest smartphone with 5G, triple camera", 699.99, 649.99, '{"storage": "128GB", "5G": true, "camera": "triple"}', 4.8, 892),
        ("SKU1005", "Wireless Mouse", "Electronics", "Ergonomic wireless mouse with precision tracking", 29.99, 24.99, '{"wireless": true, "ergonomic": true}', 4.3, 156),
        
        # Clothing
        ("SKU2001", "Men's Casual Shirt", "Clothing", "100% cotton casual shirt, available in multiple colors", 39.99, 34.99, '{"material": "cotton", "sizes": ["S", "M", "L", "XL"]}', 4.2, 89),
        ("SKU2002", "Women's Running Shoes", "Clothing", "Lightweight running shoes with cushioned sole", 79.99, 69.99, '{"type": "running", "sizes": [6, 7, 8, 9, 10]}', 4.6, 234),
        ("SKU2003", "Denim Jeans", "Clothing", "Classic fit denim jeans", 59.99, 49.99, '{"material": "denim", "fit": "classic"}', 4.4, 312),
        ("SKU2004", "Winter Jacket", "Clothing", "Warm winter jacket with hood", 129.99, 99.99, '{"season": "winter", "waterproof": true}', 4.7, 178),
        
        # Home & Kitchen
        ("SKU3001", "Coffee Maker", "Home & Kitchen", "Programmable coffee maker with 12-cup capacity", 79.99, 69.99, '{"capacity": "12 cups", "programmable": true}', 4.5, 267),
        ("SKU3002", "Blender 1000W", "Home & Kitchen", "High-power blender for smoothies and food prep", 89.99, 79.99, '{"power": "1000W", "capacity": "64oz"}', 4.4, 198),
        ("SKU3003", "Cookware Set", "Home & Kitchen", "Non-stick 10-piece cookware set", 149.99, 129.99, '{"pieces": 10, "non-stick": true}', 4.6, 421),
        
        # Sports & Outdoors
        ("SKU4001", "Yoga Mat", "Sports & Outdoors", "Premium yoga mat with carrying strap", 34.99, 29.99, '{"thickness": "6mm", "material": "TPE"}', 4.5, 534),
        ("SKU4002", "Camping Tent 4-Person", "Sports & Outdoors", "Waterproof camping tent for 4 people", 159.99, 139.99, '{"capacity": 4, "waterproof": true}', 4.7, 289),
        ("SKU4003", "Fitness Tracker", "Sports & Outdoors", "Smart fitness tracker with heart rate monitor", 49.99, 44.99, '{"heart_rate": true, "waterproof": true}', 4.3, 678),
        
        # Books
        ("SKU5001", "Bestselling Novel", "Books", "Latest bestselling fiction novel", 24.99, 19.99, '{"format": "hardcover", "pages": 352}', 4.8, 1234),
        ("SKU5002", "Cookbook Collection", "Books", "Comprehensive cookbook with 500+ recipes", 34.99, 29.99, '{"format": "hardcover", "recipes": 500}', 4.6, 456),
        
        # Beauty & Personal Care
        ("SKU6001", "Skincare Set", "Beauty & Personal Care", "Complete skincare routine set", 89.99, 79.99, '{"includes": "cleanser, toner, moisturizer, serum"}', 4.7, 789),
        ("SKU6002", "Electric Toothbrush", "Beauty & Personal Care", "Rechargeable electric toothbrush with multiple modes", 69.99, 59.99, '{"rechargeable": true, "modes": 3}', 4.5, 567),
        
        # Toys & Games
        ("SKU7001", "Board Game", "Toys & Games", "Family board game for 2-6 players", 29.99, 24.99, '{"players": "2-6", "age": "8+"}', 4.6, 345),
        ("SKU7002", "Building Blocks Set", "Toys & Games", "Creative building blocks set with 500 pieces", 49.99, 44.99, '{"pieces": 500, "age": "4+"}', 4.8, 892),
    ]
    
    for product in products:
        cursor.execute("""
            INSERT INTO products (sku, name, category, description, base_price, current_price, 
                                attributes, image_url, rating, reviews_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*product, f"https://images.example.com/{product[0]}.jpg"))
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {len(products)} products")

def seed_inventory():
    """Generate inventory data for all products across locations"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT sku FROM products")
    products = cursor.fetchall()
    
    for sku_tuple in products:
        sku = sku_tuple[0]
        # Online inventory
        cursor.execute("""
            INSERT INTO inventory (sku, location, stock_quantity, reserved_quantity, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (sku, "Online Warehouse", random.randint(50, 500), random.randint(0, 20), datetime.now().isoformat()))
        
        # Store inventory
        for location in STORE_LOCATIONS:
            stock = random.randint(0, 50)
            cursor.execute("""
                INSERT INTO inventory (sku, location, stock_quantity, reserved_quantity, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (sku, location, stock, random.randint(0, min(5, stock)), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded inventory for {len(products)} products across all locations")

def seed_promotions():
    """Generate active promotions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    promotions = [
        ("WELCOME10", "10% off for new customers", "percentage", 10, 0, 
         datetime.now().isoformat(), (datetime.now() + timedelta(days=30)).isoformat(), 1000, 0),
        ("SAVE20", "Save $20 on orders over $100", "fixed", 20, 100,
         datetime.now().isoformat(), (datetime.now() + timedelta(days=15)).isoformat(), 500, 0),
        ("FREESHIP", "Free shipping on orders over $50", "shipping", 0, 50,
         datetime.now().isoformat(), (datetime.now() + timedelta(days=60)).isoformat(), -1, 0),
        ("FLASH25", "Flash sale - 25% off electronics", "percentage", 25, 0,
         datetime.now().isoformat(), (datetime.now() + timedelta(days=3)).isoformat(), 200, 0),
    ]
    
    for promo in promotions:
        cursor.execute("""
            INSERT INTO promotions (promo_code, description, discount_type, discount_value,
                                  min_purchase, valid_from, valid_until, usage_limit, times_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, promo)
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {len(promotions)} active promotions")

def initialize_database():
    """Complete database initialization"""
    print("🔧 Initializing Retail Sales Database...")
    create_database()
    seed_customers(10)
    seed_products()
    seed_inventory()
    seed_promotions()
    print("✅ Database initialization complete!")

if __name__ == "__main__":
    initialize_database()
