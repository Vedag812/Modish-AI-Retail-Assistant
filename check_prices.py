"""Quick script to check product prices"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db import get_db

conn = get_db()
cur = conn.cursor()

print("\n📊 Sample Products by Category:\n")

categories = ['Grocery', 'Electronics', 'Beauty & Personal Care', 'Clothing']
for cat in categories:
    cur.execute("SELECT name, current_price FROM products WHERE category = %s LIMIT 3", (cat,))
    rows = cur.fetchall()
    print(f"  {cat}:")
    for r in rows:
        print(f"    - {r[0][:35]:<37} ₹{r[1]:>8,.2f}")
    print()

conn.close()
