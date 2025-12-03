"""
Recommendation Agent Tools
Analyzes customer profile, browsing history, and seasonal trends to suggest products
"""
import sqlite3
import json
import random
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DB_PATH

def get_personalized_recommendations(customer_id: str, max_recommendations: int = 5):
    """
    Get personalized product recommendations based on customer profile and history.
    
    Args:
        customer_id: The unique customer identifier (e.g., "CUST1001")
        max_recommendations: Maximum number of products to recommend (default: 5)
    
    Returns:
        Dictionary with status and recommendations
        Success: {
            "status": "success",
            "customer_name": "John Doe",
            "recommendations": [
                {
                    "sku": "SKU1001",
                    "name": "Wireless Bluetooth Headphones",
                    "category": "Electronics",
                    "price": 129.99,
                    "rating": 4.5,
                    "reason": "Based on your browsing history"
                },
                ...
            ]
        }
        Error: {"status": "error", "message": "Customer not found"}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get customer profile
    cursor.execute("""
        SELECT name, browsing_history, purchase_history, preferences
        FROM customers WHERE customer_id = ?
    """, (customer_id,))
    
    customer = cursor.fetchone()
    if not customer:
        conn.close()
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    name, browsing_json, purchase_json, preferences_json = customer
    browsing_history = json.loads(browsing_json)
    purchase_history = json.loads(purchase_json)
    preferences = json.loads(preferences_json)
    
    # Get previously viewed/purchased SKUs
    viewed_skus = browsing_history[-10:] if browsing_history else []
    purchased_skus = [item['sku'] for item in purchase_history]
    
    # Get products from favorite categories
    favorite_categories = preferences.get('favorite_categories', [])
    
    recommendations = []
    
    # Recommend from favorite categories
    if favorite_categories:
        placeholders = ','.join('?' * len(favorite_categories))
        cursor.execute(f"""
            SELECT sku, name, category, current_price, rating, reviews_count
            FROM products
            WHERE category IN ({placeholders}) AND sku NOT IN ({','.join('?' * len(purchased_skus)) if purchased_skus else '?'})
            ORDER BY rating DESC, reviews_count DESC
            LIMIT ?
        """, (*favorite_categories, *(purchased_skus if purchased_skus else ['']), max_recommendations))
        
        for row in cursor.fetchall():
            recommendations.append({
                "sku": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "rating": row[4],
                "reason": f"Recommended based on your interest in {row[2]}"
            })
    
    # Add trending products if we need more
    if len(recommendations) < max_recommendations:
        excluded_skus = [r['sku'] for r in recommendations] + purchased_skus
        if excluded_skus:
            placeholders = ','.join('?' * len(excluded_skus))
            params = tuple(excluded_skus) + (max_recommendations - len(recommendations),)
        else:
            placeholders = '?'
            params = ('', max_recommendations - len(recommendations))
        
        cursor.execute(f"""
            SELECT sku, name, category, current_price, rating, reviews_count
            FROM products
            WHERE sku NOT IN ({placeholders})
            ORDER BY rating DESC, reviews_count DESC
            LIMIT ?
        """, params)
        
        for row in cursor.fetchall():
            recommendations.append({
                "sku": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "rating": row[4],
                "reason": "Trending item with high ratings"
            })
    
    conn.close()
    
    return {
        "status": "success",
        "customer_name": name,
        "recommendations": recommendations[:max_recommendations]
    }

def suggest_bundle_deals(sku: str):
    """
    Suggest complementary products that go well together as a bundle.
    
    Args:
        sku: The product SKU to find complementary items for
    
    Returns:
        Dictionary with bundle suggestions
        Success: {
            "status": "success",
            "main_product": {"sku": "SKU1001", "name": "...", "price": 129.99},
            "bundle_items": [
                {"sku": "SKU1005", "name": "...", "price": 24.99, "discount": "10%"},
                ...
            ],
            "bundle_savings": 25.00
        }
        Error: {"status": "error", "message": "Product not found"}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get main product
    cursor.execute("""
        SELECT sku, name, category, current_price
        FROM products WHERE sku = ?
    """, (sku,))
    
    main_product = cursor.fetchone()
    if not main_product:
        conn.close()
        return {"status": "error", "message": f"Product {sku} not found"}
    
    main_sku, main_name, main_category, main_price = main_product
    
    # Get complementary products from same or related categories
    cursor.execute("""
        SELECT sku, name, current_price
        FROM products
        WHERE category = ? AND sku != ?
        ORDER BY rating DESC
        LIMIT 3
    """, (main_category, sku))
    
    bundle_items = []
    total_discount = 0
    
    for row in cursor.fetchall():
        discount_amount = round(row[2] * 0.10, 2)  # 10% bundle discount
        bundle_items.append({
            "sku": row[0],
            "name": row[1],
            "original_price": row[2],
            "bundle_price": round(row[2] - discount_amount, 2),
            "discount": "10%"
        })
        total_discount += discount_amount
    
    conn.close()
    
    return {
        "status": "success",
        "main_product": {
            "sku": main_sku,
            "name": main_name,
            "price": main_price
        },
        "bundle_items": bundle_items,
        "bundle_savings": round(total_discount, 2),
        "message": f"Save ${round(total_discount, 2)} when you buy these items together!"
    }

def get_seasonal_promotions(category: str = None):
    """
    Get current seasonal promotions and deals.
    
    Args:
        category: Optional product category to filter promotions
    
    Returns:
        Dictionary with active promotions
        Success: {
            "status": "success",
            "promotions": [
                {
                    "code": "WELCOME10",
                    "description": "10% off for new customers",
                    "discount_type": "percentage",
                    "discount_value": 10,
                    "valid_until": "2025-01-02"
                },
                ...
            ]
        }
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT promo_code, description, discount_type, discount_value, min_purchase, valid_until
        FROM promotions
        WHERE datetime(valid_until) > datetime('now')
        AND (usage_limit = -1 OR times_used < usage_limit)
    """)
    
    promotions = []
    for row in cursor.fetchall():
        promotions.append({
            "code": row[0],
            "description": row[1],
            "discount_type": row[2],
            "discount_value": row[3],
            "min_purchase": row[4],
            "valid_until": row[5].split('T')[0]
        })
    
    conn.close()
    
    return {
        "status": "success",
        "promotions": promotions,
        "count": len(promotions)
    }

print("✅ Recommendation tools loaded")
