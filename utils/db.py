"""
Database Connection Utility
Firebase Firestore Database Integration
Wrapper that provides backwards compatibility with existing code
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import Firebase module
from utils.firebase_db import (
    get_db as firebase_get_db,
    get_customer as firebase_get_customer,
    create_customer as firebase_create_customer,
    update_customer as firebase_update_customer,
    get_product as firebase_get_product,
    search_products as firebase_search_products,
    get_inventory as firebase_get_inventory,
    update_inventory as firebase_update_inventory,
    create_order as firebase_create_order,
    get_order as firebase_get_order,
    update_order as firebase_update_order,
    get_customer_orders as firebase_get_customer_orders,
    get_promotion as firebase_get_promotion,
    create_transaction as firebase_create_transaction,
    execute_query as firebase_execute_query,
)

def get_db():
    """Get Firebase database client (backwards compatible)"""
    return firebase_get_db()

def execute_query(query_func, *args, **kwargs):
    """Execute a query function (backwards compatible wrapper)"""
    return firebase_execute_query(query_func, *args, **kwargs)

def get_customer(customer_id):
    """Get customer by ID"""
    return firebase_get_customer(customer_id)

def create_customer(customer_id, name, email, phone="", location="", tier="Bronze", points=0):
    """Create a new customer in the database"""
    customer_data = {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "loyalty_tier": tier,
        "loyalty_points": points,
        "browsing_history": [],
        "purchase_history": [],
        "preferences": {}
    }
    result = firebase_create_customer(customer_data)
    if result.get("status") == "success":
        return {"status": "success", "message": f"Customer {customer_id} created successfully", "customer_id": customer_id}
    return result

def update_customer_points(customer_id, points_to_add):
    """Update customer loyalty points"""
    customer = firebase_get_customer(customer_id)
    if customer:
        new_points = customer.get("loyalty_points", 0) + points_to_add
        firebase_update_customer(customer_id, {"loyalty_points": new_points})

def update_customer_tier(customer_id, new_tier):
    """Update customer loyalty tier"""
    firebase_update_customer(customer_id, {"loyalty_tier": new_tier})

def get_product(sku):
    """Get product by SKU"""
    return firebase_get_product(sku)

def search_products(query="", category="", min_price=None, max_price=None, limit=10):
    """Search products by name, category, price range"""
    return firebase_search_products(query, category, min_price, max_price, limit)

def get_inventory(sku, location=None):
    """Get inventory for a product"""
    return firebase_get_inventory(sku, location)

def get_promotions():
    """Get all active promotions"""
    from utils.firebase_db import get_promotions as firebase_get_promotions
    return firebase_get_promotions()

def generate_customer_id():
    """Generate a new unique customer ID"""
    from utils.firebase_db import get_all_customers
    customers = get_all_customers(limit=1000)
    if customers:
        max_num = 1000
        for c in customers:
            cid = c.get("customer_id", "CUST1000")
            try:
                num = int(cid.replace("CUST", ""))
                if num > max_num:
                    max_num = num
            except:
                pass
        return f"CUST{max_num + 1:04d}"
    return "CUST1001"

print("✅ Firebase database module loaded")
