"""
PostgreSQL Database Connection Utility
Uses Neon Cloud PostgreSQL ONLY - No local SQLite
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found! Please set it in .env file")

def get_db():
    """Get PostgreSQL database connection"""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute a query and optionally fetch results"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
            conn.close()
            return result
        elif fetch_all:
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def get_customer(customer_id):
    """Get customer by ID"""
    result = execute_query(
        """SELECT customer_id, name, email, phone, location, loyalty_tier, loyalty_points,
                  browsing_history, purchase_history, preferences
           FROM customers WHERE customer_id = %s""",
        (customer_id,),
        fetch_one=True
    )
    if result:
        return {
            "customer_id": result[0],
            "name": result[1],
            "email": result[2],
            "phone": result[3],
            "location": result[4],
            "loyalty_tier": result[5],
            "loyalty_points": result[6],
            "browsing_history": json.loads(result[7]) if result[7] else [],
            "purchase_history": json.loads(result[8]) if result[8] else [],
            "preferences": json.loads(result[9]) if result[9] else {}
        }
    return None

def create_customer(customer_id, name, email, phone="", location="", tier="Bronze", points=0):
    """Create a new customer in the database"""
    try:
        execute_query(
            """INSERT INTO customers 
               (customer_id, name, email, phone, location, loyalty_tier, loyalty_points, browsing_history, purchase_history, preferences)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (customer_id, name, email, phone, location, tier, points, '[]', '[]', '{}')
        )
        return {"status": "success", "message": f"Customer {customer_id} created successfully", "customer_id": customer_id}
    except psycopg2.IntegrityError:
        return {"status": "error", "message": f"Customer {customer_id} or email already exists"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_customer_points(customer_id, points_to_add):
    """Update customer loyalty points"""
    execute_query(
        "UPDATE customers SET loyalty_points = loyalty_points + %s WHERE customer_id = %s",
        (points_to_add, customer_id)
    )

def update_customer_tier(customer_id, new_tier):
    """Update customer loyalty tier"""
    execute_query(
        "UPDATE customers SET loyalty_tier = %s WHERE customer_id = %s",
        (new_tier, customer_id)
    )

def get_product(sku):
    """Get product by SKU"""
    result = execute_query(
        "SELECT sku, name, category, current_price, rating, reviews_count FROM products WHERE sku = %s",
        (sku,),
        fetch_one=True
    )
    if result:
        return {
            "sku": result[0],
            "name": result[1],
            "category": result[2],
            "price": float(result[3]),
            "rating": float(result[4]) if result[4] else 0,
            "reviews": result[5] or 0
        }
    return None

def search_products(query="", category="", min_price=None, max_price=None, limit=10):
    """Search products by name, category, price range"""
    sql = "SELECT sku, name, category, current_price, rating, reviews_count FROM products WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (LOWER(name) LIKE %s OR LOWER(category) LIKE %s)"
        search_term = f"%{query.lower()}%"
        params.extend([search_term, search_term])
    
    if category:
        sql += " AND LOWER(category) = %s"
        params.append(category.lower())
    
    if min_price is not None:
        sql += " AND current_price >= %s"
        params.append(min_price)
    
    if max_price is not None:
        sql += " AND current_price <= %s"
        params.append(max_price)
    
    sql += " ORDER BY rating DESC, reviews_count DESC LIMIT %s"
    params.append(limit)
    
    results = execute_query(sql, params, fetch_all=True)
    
    return [{
        "sku": r[0],
        "name": r[1],
        "category": r[2],
        "price": float(r[3]),
        "rating": float(r[4]) if r[4] else 0,
        "reviews": r[5] or 0
    } for r in results]

def get_inventory(sku, location=None):
    """Get inventory for a product"""
    if location:
        result = execute_query(
            "SELECT location, quantity FROM inventory WHERE sku = %s AND location = %s",
            (sku, location),
            fetch_one=True
        )
        if result:
            return [{"location": result[0], "quantity": result[1]}]
        return []
    else:
        results = execute_query(
            "SELECT location, quantity FROM inventory WHERE sku = %s",
            (sku,),
            fetch_all=True
        )
        return [{"location": r[0], "quantity": r[1]} for r in results]

def get_promotions():
    """Get all active promotions"""
    results = execute_query(
        "SELECT promo_code, description, discount_percent, min_order_value, valid_until FROM promotions",
        fetch_all=True
    )
    return [{
        "code": r[0],
        "description": r[1],
        "discount_percent": float(r[2]) if r[2] else 0,
        "min_order": float(r[3]) if r[3] else 0,
        "valid_until": str(r[4]) if r[4] else None
    } for r in results]

def generate_customer_id():
    """Generate a new unique customer ID"""
    result = execute_query(
        "SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1",
        fetch_one=True
    )
    if result:
        last_id = result[0]
        num = int(last_id.replace("CUST", "")) + 1
        return f"CUST{num:04d}"
    return "CUST1001"

print("✅ PostgreSQL database module loaded (Neon Cloud)")
