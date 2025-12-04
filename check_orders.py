"""Check recent orders in database"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db import get_db

conn = get_db()
cur = conn.cursor()

print("\n📊 Recent Orders in Database:\n")
cur.execute("""
    SELECT order_id, customer_id, total_amount, status, created_at 
    FROM orders 
    ORDER BY created_at DESC 
    LIMIT 10
""")

orders = cur.fetchall()
if orders:
    for r in orders:
        print(f"  {r[0]}: Customer {r[1]}, ₹{r[2]:.2f}, Status: {r[3].upper()}, Created: {r[4]}")
else:
    print("  No orders found!")

print("\n📦 Order Items:")
cur.execute("""
    SELECT oi.order_id, oi.sku, oi.product_name, oi.quantity, oi.price
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    ORDER BY o.created_at DESC
    LIMIT 10
""")

items = cur.fetchall()
if items:
    for r in items:
        print(f"  {r[0]}: {r[2]} (SKU: {r[1]}) x{r[3]} = ₹{r[4]:.2f}")
else:
    print("  No order items found!")

conn.close()
