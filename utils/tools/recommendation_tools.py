"""
Recommendation Agent Tools
Analyzes customer profile, browsing history, and seasonal trends to suggest products
Uses PostgreSQL (Neon Cloud) ONLY
"""
import json
import random
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.db import get_db, execute_query, get_customer, search_products, get_promotions

def get_personalized_recommendations(customer_id: str, max_recommendations: int = 5):
    """
    Get personalized product recommendations based on customer profile and history.
    
    Args:
        customer_id: The unique customer identifier (e.g., "CUST1001")
        max_recommendations: Maximum number of products to recommend (default: 5)
    
    Returns:
        Dictionary with status and recommendations
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    name = customer["name"]
    browsing_history = customer.get("browsing_history", [])
    purchase_history = customer.get("purchase_history", [])
    preferences = customer.get("preferences", {})
    
    # Get previously purchased SKUs
    purchased_skus = [item.get('sku', '') for item in purchase_history] if purchase_history else []
    
    # Get products from favorite categories
    favorite_categories = preferences.get('favorite_categories', [])
    
    recommendations = []
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Recommend from favorite categories
    if favorite_categories:
        placeholders = ','.join(['%s'] * len(favorite_categories))
        exclude_placeholders = ','.join(['%s'] * len(purchased_skus)) if purchased_skus else '%s'
        
        cursor.execute(f"""
            SELECT sku, name, category, current_price, rating, reviews_count
            FROM products
            WHERE category IN ({placeholders}) AND sku NOT IN ({exclude_placeholders})
            ORDER BY rating DESC, reviews_count DESC
            LIMIT %s
        """, (*favorite_categories, *(purchased_skus if purchased_skus else ['']), max_recommendations))
        
        for row in cursor.fetchall():
            recommendations.append({
                "sku": row[0],
                "name": row[1],
                "category": row[2],
                "price": float(row[3]),
                "rating": float(row[4]) if row[4] else 0,
                "reason": f"Recommended based on your interest in {row[2]}"
            })
    
    # Add trending products if we need more
    if len(recommendations) < max_recommendations:
        excluded_skus = [r['sku'] for r in recommendations] + purchased_skus
        if excluded_skus:
            placeholders = ','.join(['%s'] * len(excluded_skus))
            params = tuple(excluded_skus) + (max_recommendations - len(recommendations),)
        else:
            placeholders = '%s'
            params = ('', max_recommendations - len(recommendations))
        
        cursor.execute(f"""
            SELECT sku, name, category, current_price, rating, reviews_count
            FROM products
            WHERE sku NOT IN ({placeholders})
            ORDER BY rating DESC, reviews_count DESC
            LIMIT %s
        """, params)
        
        for row in cursor.fetchall():
            recommendations.append({
                "sku": row[0],
                "name": row[1],
                "category": row[2],
                "price": float(row[3]),
                "rating": float(row[4]) if row[4] else 0,
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
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Get main product
    cursor.execute("""
        SELECT sku, name, category, current_price
        FROM products WHERE sku = %s
    """, (sku,))
    
    main_product = cursor.fetchone()
    if not main_product:
        conn.close()
        return {"status": "error", "message": f"Product {sku} not found"}
    
    main_sku, main_name, main_category, main_price = main_product
    
    # Get complementary products from same category
    cursor.execute("""
        SELECT sku, name, current_price
        FROM products
        WHERE category = %s AND sku != %s
        ORDER BY rating DESC
        LIMIT 3
    """, (main_category, sku))
    
    bundle_items = []
    total_discount = 0
    
    for row in cursor.fetchall():
        discount_amount = round(float(row[2]) * 0.10, 2)
        bundle_items.append({
            "sku": row[0],
            "name": row[1],
            "original_price": float(row[2]),
            "bundle_price": round(float(row[2]) - discount_amount, 2),
            "discount": "10%"
        })
        total_discount += discount_amount
    
    conn.close()
    
    return {
        "status": "success",
        "main_product": {
            "sku": main_sku,
            "name": main_name,
            "price": float(main_price)
        },
        "bundle_items": bundle_items,
        "bundle_savings": round(total_discount, 2),
        "message": f"Save ${round(total_discount, 2)} when you buy these items together!"
    }

def get_seasonal_promotions(category: str = None):
    """
    Get current seasonal promotions and deals.
    """
    promotions = get_promotions()
    return {
        "status": "success",
        "promotions": promotions,
        "count": len(promotions)
    }

def search_products_tool(query: str = "", category: str = "", max_price: float = None, min_price: float = None, max_results: int = 10):
    """Search for products by name, category, and price range."""
    results = search_products(query=query, category=category, min_price=min_price, max_price=max_price, limit=max_results)
    
    return {
        "status": "success",
        "results": results,
        "count": len(results),
        "query": query,
        "filters": {"category": category, "max_price": max_price, "min_price": min_price}
    }

print("✅ Recommendation tools loaded (PostgreSQL)")
