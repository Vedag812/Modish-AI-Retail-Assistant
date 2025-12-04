"""
Populate Neon PostgreSQL with Indian dataset:
- 200 products (Indian-focused names & categories)
- 30+ Indian customers
- Inventory across Indian warehouse locations

Usage: python data/populate_india_dataset.py
"""
import json
import sys
import os
from datetime import datetime

# Ensure project root is on sys.path so `utils` package imports work when run as a script
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.db import get_db


def clear_old_data(conn):
    """Clear old data to make way for Indian dataset"""
    cursor = conn.cursor()
    print("🗑️  Clearing old data...")
    try:
        # Delete in correct order for foreign key constraints
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM promotions") 
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")
        conn.commit()
        print("✅ Old data cleared")
    except Exception as e:
        print(f"⚠️  Warning clearing data: {e}")
        conn.rollback()

CITIES = [
    "Mumbai, Maharashtra",
    "Delhi, NCR",
    "Bengaluru, Karnataka",
    "Chennai, Tamil Nadu",
    "Hyderabad, Telangana",
    "Kolkata, West Bengal",
    "Pune, Maharashtra",
    "Ahmedabad, Gujarat",
    "Surat, Gujarat",
    "Jaipur, Rajasthan"
]

WAREHOUSES = [
    "Mumbai Warehouse",
    "Delhi Warehouse",
    "Bengaluru Warehouse",
    "Chennai Warehouse",
    "Hyderabad Warehouse",
]

CATEGORIES = [
    "Electronics", "Home & Kitchen", "Clothing", "Footwear", "Beauty & Personal Care",
    "Grocery", "Sports & Outdoors", "Toys & Games", "Automotive", "Mobile Accessories"
]

# Base names per category to generate products
BASE_PRODUCTS = {
    "Electronics": [
        "Smart LED TV", "Bluetooth Earbuds", "Soundbar", "Portable Speaker", "Smartwatch", "Android Phone",
        "Laptop", "Tablet", "Wireless Charger", "Action Camera"
    ],
    "Home & Kitchen": [
        "Non-stick Cookware Set", "Mixer Grinder", "Electric Kettle", "Air Fryer", "Pressure Cooker",
        "Vacuum Cleaner", "Microfiber Bedsheet", "Dining Set", "LED Bulb Pack", "Ceiling Fan"
    ],
    "Clothing": [
        "Men's Kurta", "Women's Saree", "Casual Shirt", "Jeans", "T-shirt", "Ethnic Kurti", "Blazer",
        "Leggings", "Salwar Suit", "Winter Jacket"
    ],
    "Footwear": [
        "Running Shoes", "Formal Shoes", "Casual Sneakers", "Flip Flops", "Leather Sandals"
    ],
    "Beauty & Personal Care": [
        "Hair Oil", "Face Wash", "Moisturizer", "Perfume", "Shampoo", "Conditioner", "Makeup Kit"
    ],
    "Grocery": [
        "Basmati Rice 5kg", "Toor Dal 1kg", "Refined Oil 1L", "Tea Powder 500g", "Organic Honey 250g",
        "Spice Mix", "Atta 5kg", "Sugar 2kg"
    ],
    "Sports & Outdoors": [
        "Yoga Mat", "Cricket Bat", "Badminton Racket", "Dumbbell Set", "Cycling Helmet"
    ],
    "Toys & Games": [
        "Wooden Puzzle", "Educational Board Game", "Remote Car", "Building Blocks", "Doll Set"
    ],
    "Automotive": [
        "Car Seat Cover", "Car Air Freshener", "Bike Helmet", "Car Vacuum Cleaner", "Jump Starter"
    ],
    "Mobile Accessories": [
        "Phone Case", "Tempered Glass", "Power Bank", "USB C Cable", "Wireless Earbuds Case"
    ]
}

CUSTOMERS = [
    {"customer_id": "CUST2001", "name": "Amit Verma", "email": "amit.verma@gmail.com", "phone": "+91-9000000001", "location": "Mumbai, Maharashtra", "loyalty_tier": "Platinum", "loyalty_points": 4200},
    {"customer_id": "CUST2002", "name": "Neha Reddy", "email": "neha.reddy@gmail.com", "phone": "+91-9000000002", "location": "Bengaluru, Karnataka", "loyalty_tier": "Gold", "loyalty_points": 2100},
    {"customer_id": "CUST2003", "name": "Rohit Sharma", "email": "rohit.sharma@gmail.com", "phone": "+91-9000000003", "location": "Delhi, NCR", "loyalty_tier": "Silver", "loyalty_points": 950},
    {"customer_id": "CUST2004", "name": "Priya Singh", "email": "priya.singh@gmail.com", "phone": "+91-9000000004", "location": "Chennai, Tamil Nadu", "loyalty_tier": "Gold", "loyalty_points": 1800},
    {"customer_id": "CUST2005", "name": "Suresh Kumar", "email": "suresh.kumar@gmail.com", "phone": "+91-9000000005", "location": "Hyderabad, Telangana", "loyalty_tier": "Bronze", "loyalty_points": 300},
    {"customer_id": "CUST2006", "name": "Anjali Gupta", "email": "anjali.gupta@gmail.com", "phone": "+91-9000000006", "location": "Pune, Maharashtra", "loyalty_tier": "Gold", "loyalty_points": 2400},
    {"customer_id": "CUST2007", "name": "Vikram Patel", "email": "vikram.patel@gmail.com", "phone": "+91-9000000007", "location": "Ahmedabad, Gujarat", "loyalty_tier": "Silver", "loyalty_points": 1100},
    {"customer_id": "CUST2008", "name": "Sana Khan", "email": "sana.khan@gmail.com", "phone": "+91-9000000008", "location": "Lucknow, Uttar Pradesh", "loyalty_tier": "Bronze", "loyalty_points": 400},
    {"customer_id": "CUST2009", "name": "Manish Desai", "email": "manish.desai@gmail.com", "phone": "+91-9000000009", "location": "Vadodara, Gujarat", "loyalty_tier": "Gold", "loyalty_points": 1750},
    {"customer_id": "CUST2010", "name": "Kavya Nair", "email": "kavya.nair@gmail.com", "phone": "+91-9000000010", "location": "Kochi, Kerala", "loyalty_tier": "Silver", "loyalty_points": 980},
    {"customer_id": "CUST2011", "name": "Arjun Mehta", "email": "arjun.mehta@gmail.com", "phone": "+91-9000000011", "location": "Jaipur, Rajasthan", "loyalty_tier": "Gold", "loyalty_points": 2000},
    {"customer_id": "CUST2012", "name": "Meera Iyer", "email": "meera.iyer@gmail.com", "phone": "+91-9000000012", "location": "Coimbatore, Tamil Nadu", "loyalty_tier": "Bronze", "loyalty_points": 150},
    {"customer_id": "CUST2013", "name": "Kabir Khan", "email": "kabir.khan@gmail.com", "phone": "+91-9000000013", "location": "Bhopal, Madhya Pradesh", "loyalty_tier": "Silver", "loyalty_points": 860},
    {"customer_id": "CUST2014", "name": "Ritika Bose", "email": "ritika.bose@gmail.com", "phone": "+91-9000000014", "location": "Kolkata, West Bengal", "loyalty_tier": "Gold", "loyalty_points": 1900},
    {"customer_id": "CUST2015", "name": "Aditya Rao", "email": "aditya.rao@gmail.com", "phone": "+91-9000000015", "location": "Mysuru, Karnataka", "loyalty_tier": "Bronze", "loyalty_points": 230},
    {"customer_id": "CUST2016", "name": "Sneha Kapoor", "email": "sneha.kapoor@gmail.com", "phone": "+91-9000000016", "location": "Gurgaon, Haryana", "loyalty_tier": "Gold", "loyalty_points": 2600},
    {"customer_id": "CUST2017", "name": "Praveen Kumar", "email": "praveen.kumar@gmail.com", "phone": "+91-9000000017", "location": "Chandigarh, Punjab", "loyalty_tier": "Silver", "loyalty_points": 720},
    {"customer_id": "CUST2018", "name": "Isha Malhotra", "email": "isha.malhotra@gmail.com", "phone": "+91-9000000018", "location": "Indore, Madhya Pradesh", "loyalty_tier": "Gold", "loyalty_points": 1550},
    {"customer_id": "CUST2019", "name": "Soham Patil", "email": "soham.patil@gmail.com", "phone": "+91-9000000019", "location": "Nagpur, Maharashtra", "loyalty_tier": "Bronze", "loyalty_points": 410},
    {"customer_id": "CUST2020", "name": "Nisha Sharma", "email": "nisha.sharma@gmail.com", "phone": "+91-9000000020", "location": "Ranchi, Jharkhand", "loyalty_tier": "Silver", "loyalty_points": 640},
    {"customer_id": "CUST2021", "name": "Ankit Joshi", "email": "ankit.joshi@gmail.com", "phone": "+91-9000000021", "location": "Dehradun, Uttarakhand", "loyalty_tier": "Gold", "loyalty_points": 2100},
    {"customer_id": "CUST2022", "name": "Pooja Yadav", "email": "pooja.yadav@gmail.com", "phone": "+91-9000000022", "location": "Patna, Bihar", "loyalty_tier": "Bronze", "loyalty_points": 120},
    {"customer_id": "CUST2023", "name": "Harish Chandra", "email": "harish.chandra@gmail.com", "phone": "+91-9000000023", "location": "Surat, Gujarat", "loyalty_tier": "Silver", "loyalty_points": 880},
    {"customer_id": "CUST2024", "name": "Geeta Rani", "email": "geeta.rani@gmail.com", "phone": "+91-9000000024", "location": "Jodhpur, Rajasthan", "loyalty_tier": "Bronze", "loyalty_points": 270},
    {"customer_id": "CUST2025", "name": "Vivek Nambiar", "email": "vivek.nambiar@gmail.com", "phone": "+91-9000000025", "location": "Thiruvananthapuram, Kerala", "loyalty_tier": "Gold", "loyalty_points": 2350},
    {"customer_id": "CUST2026", "name": "Latha R", "email": "latha.r@gmail.com", "phone": "+91-9000000026", "location": "Mangalore, Karnataka", "loyalty_tier": "Silver", "loyalty_points": 980},
    {"customer_id": "CUST2027", "name": "Ramesh Babu", "email": "ramesh.babu@gmail.com", "phone": "+91-9000000027", "location": "Vijayawada, Andhra Pradesh", "loyalty_tier": "Bronze", "loyalty_points": 360},
    {"customer_id": "CUST2028", "name": "Shweta Goyal", "email": "shweta.goyal@gmail.com", "phone": "+91-9000000028", "location": "Faridabad, Haryana", "loyalty_tier": "Gold", "loyalty_points": 1980},
    {"customer_id": "CUST2029", "name": "Karan B", "email": "karan.b@gmail.com", "phone": "+91-9000000029", "location": "Noida, Uttar Pradesh", "loyalty_tier": "Silver", "loyalty_points": 740},
    {"customer_id": "CUST2030", "name": "Tulsi Das", "email": "tulsi.das@gmail.com", "phone": "+91-9000000030", "location": "Dibrugarh, Assam", "loyalty_tier": "Bronze", "loyalty_points": 95},
]


# Realistic price ranges per category (in INR)
PRICE_RANGES = {
    "Electronics": (4999, 49999),
    "Home & Kitchen": (299, 9999),
    "Clothing": (299, 4999),
    "Footwear": (499, 5999),
    "Beauty & Personal Care": (99, 2499),
    "Grocery": (49, 999),
    "Sports & Outdoors": (199, 4999),
    "Toys & Games": (199, 2999),
    "Automotive": (199, 4999),
    "Mobile Accessories": (99, 1999)
}

def generate_products(count=200):
    products = []
    sku_num = 1001
    import random
    for _ in range(count):
        category = random.choice(CATEGORIES)
        base = random.choice(BASE_PRODUCTS[category])
        variant = random.choice(["", " - With Warranty", " (New)", " - 2025 Edition", " - Combo Pack"]) 
        name = base + variant
        min_price, max_price = PRICE_RANGES.get(category, (199, 4999))
        price = round(random.uniform(min_price, max_price), 2)
        rating = round(random.uniform(3.5, 5.0), 1)
        reviews = random.randint(5, 12000)
        sku = f"IND{sku_num}"
        sku_num += 1
        products.append({
            "sku": sku,
            "name": name,
            "category": category,
            "current_price": price,
            "rating": rating,
            "reviews_count": reviews
        })
    return products


def upsert_products(conn, products):
    cursor = conn.cursor()
    for p in products:
        cursor.execute(
            """
            INSERT INTO products (sku, name, category, current_price, rating, reviews_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sku) DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                current_price = EXCLUDED.current_price,
                rating = EXCLUDED.rating,
                reviews_count = EXCLUDED.reviews_count
            """,
            (p["sku"], p["name"], p["category"], p["current_price"], p["rating"], p["reviews_count"], datetime.now())
        )
    conn.commit()


def upsert_customers(conn, customers):
    cursor = conn.cursor()
    for c in customers:
        cursor.execute(
            """
            INSERT INTO customers (customer_id, name, email, phone, location, loyalty_tier, loyalty_points, browsing_history, purchase_history, preferences, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                phone = EXCLUDED.phone,
                location = EXCLUDED.location,
                loyalty_tier = EXCLUDED.loyalty_tier,
                loyalty_points = EXCLUDED.loyalty_points
            """,
            (c["customer_id"], c["name"], c["email"], c["phone"], c["location"], c["loyalty_tier"], c["loyalty_points"], '[]', '[]', '{}', datetime.now())
        )
    conn.commit()


def upsert_inventory(conn, products, warehouses):
    cursor = conn.cursor()
    import random
    for p in products:
        for w in warehouses:
            qty = random.randint(20, 500) if w == "Mumbai Warehouse" else random.randint(5, 200)
            cursor.execute(
                """
                INSERT INTO inventory (sku, location, quantity, last_updated)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (sku, location) DO UPDATE SET quantity = EXCLUDED.quantity, last_updated = EXCLUDED.last_updated
                """,
                (p["sku"], w, qty, datetime.now())
            )
    conn.commit()


def add_promotions(conn):
    cursor = conn.cursor()
    promos = [
        ("INDWELCOME50", "₹50 off on first order", None, 50.0, 0, None),
        ("DIWALI20", "20% off for Diwali sale", 20.0, None, 500, None),
        ("FESTIVE100", "Flat ₹100 off above ₹2000", None, 100.0, 2000, None),
    ]
    for p in promos:
        cursor.execute(
            """
            INSERT INTO promotions (promo_code, description, discount_percent, discount_amount, min_purchase, valid_until)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (promo_code) DO UPDATE SET description = EXCLUDED.description, discount_percent = EXCLUDED.discount_percent, discount_amount = EXCLUDED.discount_amount, min_purchase = EXCLUDED.min_purchase
            """,
            p
        )
    conn.commit()


def check_data_exists(conn):
    """Check if Indian dataset already exists"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE sku LIKE 'IND%'")
    count = cursor.fetchone()[0]
    return count >= 1000  # If we have 1000+ Indian products, data exists


def main(force_reload=False):
    """
    Populate database with Indian dataset.
    Skips if data already exists unless force_reload=True.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if data already exists
    if not force_reload and check_data_exists(conn):
        cursor.execute("SELECT COUNT(*) FROM products")
        prod_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM customers")
        cust_count = cursor.fetchone()[0]
        print(f"✅ Database ready: {prod_count} products, {cust_count} customers")
        conn.close()
        return
    
    print("\n🚀 Initializing Indian Dataset...\n")
    
    # Clear old data first
    clear_old_data(conn)
    
    products = generate_products(200)
    print(f"   Generated {len(products)} products")
    upsert_products(conn, products)
    print("   ✅ Products inserted")
    
    upsert_customers(conn, CUSTOMERS)
    print(f"   ✅ {len(CUSTOMERS)} customers upserted")
    
    upsert_inventory(conn, products, WAREHOUSES)
    print(f"   ✅ Inventory added across {len(WAREHOUSES)} Indian warehouses")
    
    add_promotions(conn)
    print("   ✅ Indian promotions added")
    
    # Show actual counts from database
    cursor.execute("SELECT COUNT(*) FROM products")
    prod_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    cust_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM inventory")
    inv_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM promotions")
    promo_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n🎉 Database Ready!")
    print(f"   📊 Products: {prod_count}")
    print(f"   👥 Customers: {cust_count}")
    print(f"   🏪 Inventory entries: {inv_count}")
    print(f"   🎁 Promotions: {promo_count}\n")

if __name__ == '__main__':
    main()
