"""Display sample products from each category"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_db

conn = get_db()
cur = conn.cursor()

print("\n" + "="*70)
print("📊 1200+ INDIAN PRODUCTS DATABASE - SAMPLE")
print("="*70)

# Get categories
cur.execute("SELECT DISTINCT category FROM products ORDER BY category")
categories = [r[0] for r in cur.fetchall()]

for cat in categories:
    cur.execute("""
        SELECT sku, name, current_price, rating 
        FROM products 
        WHERE category = %s 
        ORDER BY RANDOM() 
        LIMIT 5
    """, (cat,))
    products = cur.fetchall()
    
    print(f"\n🏷️  {cat} (100 products)")
    print("-" * 50)
    for p in products:
        print(f"   {p[0]}: {p[1][:40]:<40} ₹{p[2]:>8,.2f}  ⭐{p[3]}")

# Summary
cur.execute("SELECT COUNT(*) FROM products")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM inventory")
inv = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM customers")
cust = cur.fetchone()[0]

print("\n" + "="*70)
print(f"📦 Total Products: {total}")
print(f"🏪 Inventory Entries: {inv} (across 5 warehouses)")
print(f"👥 Customers: {cust}")
print(f"📁 Categories: {len(categories)}")
print("="*70 + "\n")

conn.close()
