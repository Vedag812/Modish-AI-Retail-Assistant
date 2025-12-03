"""
Loyalty and Offers Agent Tools
Applies loyalty points, coupon codes, and personalized offers
"""
import sqlite3
import json
import random
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DB_PATH, LOYALTY_TIERS

def get_loyalty_status(customer_id: str):
    """
    Get customer's loyalty tier and points balance.
    
    Args:
        customer_id: Customer identifier
    
    Returns:
        Dictionary with loyalty information
        Success: {
            "status": "success",
            "customer_id": "CUST1001",
            "customer_name": "John Doe",
            "loyalty_tier": "gold",
            "points_balance": 1850,
            "points_to_next_tier": 150,
            "next_tier": "platinum",
            "tier_benefits": {
                "discount": "15%",
                "free_shipping": true,
                "early_access": true
            }
        }
        Error: {"status": "error", "message": "Customer not found"}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, loyalty_tier, loyalty_points
        FROM customers WHERE customer_id = ?
    """, (customer_id,))
    
    customer = cursor.fetchone()
    conn.close()
    
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    name, tier, points = customer
    
    # Calculate next tier
    tier_order = ["bronze", "silver", "gold", "platinum"]
    current_tier_index = tier_order.index(tier)
    next_tier = tier_order[current_tier_index + 1] if current_tier_index < len(tier_order) - 1 else None
    
    points_to_next = 0
    if next_tier:
        points_to_next = LOYALTY_TIERS[next_tier]["min_points"] - points
    
    tier_benefits = {
        "discount": f"{int(LOYALTY_TIERS[tier]['discount'] * 100)}%",
        "free_shipping": tier in ["gold", "platinum"],
        "early_access": tier in ["platinum"],
        "birthday_bonus": tier in ["silver", "gold", "platinum"],
        "exclusive_events": tier == "platinum"
    }
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "customer_name": name,
        "loyalty_tier": tier,
        "points_balance": points,
        "points_to_next_tier": max(0, points_to_next),
        "next_tier": next_tier,
        "tier_benefits": tier_benefits,
        "tier_discount": LOYALTY_TIERS[tier]["discount"]
    }

def apply_loyalty_discount(customer_id: str, order_total: float):
    """
    Apply loyalty tier discount to order total.
    
    Args:
        customer_id: Customer identifier
        order_total: Original order total
    
    Returns:
        Dictionary with discount applied
        Success: {
            "status": "success",
            "original_total": 129.99,
            "discount_percentage": 15,
            "discount_amount": 19.50,
            "final_total": 110.49,
            "points_earned": 110
        }
    """
    loyalty_info = get_loyalty_status(customer_id)
    
    if loyalty_info["status"] == "error":
        return loyalty_info
    
    discount_rate = loyalty_info["tier_discount"]
    discount_amount = order_total * discount_rate
    final_total = order_total - discount_amount
    
    # Earn 1 point per dollar spent (after discount)
    points_earned = int(final_total)
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "loyalty_tier": loyalty_info["loyalty_tier"],
        "original_total": round(order_total, 2),
        "discount_percentage": int(discount_rate * 100),
        "discount_amount": round(discount_amount, 2),
        "final_total": round(final_total, 2),
        "points_earned": points_earned,
        "message": f"Your {loyalty_info['loyalty_tier'].title()} tier discount of {int(discount_rate * 100)}% has been applied!"
    }

def apply_promo_code(promo_code: str, order_total: float, order_items: list = None):
    """
    Apply a promotional code to an order.
    
    Args:
        promo_code: Promotion code to apply
        order_total: Order total before discount
        order_items: List of items in order (for category-specific promos)
    
    Returns:
        Dictionary with promo code application result
        Success: {
            "status": "success",
            "promo_code": "SAVE20",
            "discount_type": "fixed",
            "discount_amount": 20.00,
            "new_total": 109.99
        }
        Error: {"status": "error", "message": "Invalid or expired promo code"}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT promo_code, description, discount_type, discount_value, min_purchase, 
               valid_until, usage_limit, times_used
        FROM promotions
        WHERE promo_code = ? AND datetime(valid_until) > datetime('now')
    """, (promo_code.upper(),))
    
    promo = cursor.fetchone()
    
    if not promo:
        conn.close()
        return {
            "status": "error",
            "message": f"Promo code '{promo_code}' is invalid or expired"
        }
    
    code, description, discount_type, discount_value, min_purchase, valid_until, usage_limit, times_used = promo
    
    # Check usage limit
    if usage_limit != -1 and times_used >= usage_limit:
        conn.close()
        return {
            "status": "error",
            "message": f"Promo code '{promo_code}' has reached its usage limit"
        }
    
    # Check minimum purchase
    if order_total < min_purchase:
        conn.close()
        return {
            "status": "error",
            "message": f"Order total must be at least ${min_purchase:.2f} to use this promo code"
        }
    
    # Calculate discount
    discount_amount = 0
    new_total = order_total
    
    if discount_type == "percentage":
        discount_amount = order_total * (discount_value / 100)
        new_total = order_total - discount_amount
    elif discount_type == "fixed":
        discount_amount = min(discount_value, order_total)
        new_total = order_total - discount_amount
    elif discount_type == "shipping":
        discount_amount = 0  # Handled separately in shipping calculation
        new_total = order_total
    
    # Update usage count
    cursor.execute("""
        UPDATE promotions SET times_used = times_used + 1
        WHERE promo_code = ?
    """, (promo_code.upper(),))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "promo_code": code,
        "description": description,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "discount_amount": round(discount_amount, 2),
        "original_total": round(order_total, 2),
        "new_total": round(new_total, 2),
        "message": f"Promo code '{code}' applied successfully! {description}"
    }

def calculate_final_pricing(customer_id: str, order_total: float, promo_code: str = None, items: list = None):
    """
    Calculate final pricing with all discounts and loyalty benefits.
    
    Args:
        customer_id: Customer identifier
        order_total: Base order total
        promo_code: Optional promo code
        items: List of order items
    
    Returns:
        Dictionary with complete pricing breakdown
        Success: {
            "status": "success",
            "subtotal": 129.99,
            "loyalty_discount": 19.50,
            "promo_discount": 20.00,
            "tax": 9.05,
            "shipping": 0,
            "total": 99.54,
            "total_savings": 39.50
        }
    """
    pricing = {
        "subtotal": round(order_total, 2),
        "loyalty_discount": 0,
        "promo_discount": 0,
        "tax": 0,
        "shipping": 5.99,
        "total": 0,
        "total_savings": 0
    }
    
    current_total = order_total
    
    # Apply loyalty discount
    loyalty_result = apply_loyalty_discount(customer_id, current_total)
    if loyalty_result["status"] == "success":
        pricing["loyalty_discount"] = loyalty_result["discount_amount"]
        current_total = loyalty_result["final_total"]
        pricing["points_earned"] = loyalty_result["points_earned"]
        
        # Free shipping for gold/platinum
        if loyalty_result["loyalty_tier"] in ["gold", "platinum"]:
            pricing["shipping"] = 0
    
    # Apply promo code
    if promo_code:
        promo_result = apply_promo_code(promo_code, current_total, items)
        if promo_result["status"] == "success":
            pricing["promo_discount"] = promo_result["discount_amount"]
            current_total = promo_result["new_total"]
            
            # Handle free shipping promos
            if promo_result["discount_type"] == "shipping":
                pricing["shipping"] = 0
    
    # Calculate tax (8% for example)
    pricing["tax"] = round(current_total * 0.08, 2)
    
    # Calculate final total
    pricing["total"] = round(current_total + pricing["tax"] + pricing["shipping"], 2)
    pricing["total_savings"] = round(pricing["loyalty_discount"] + pricing["promo_discount"], 2)
    
    return {
        "status": "success",
        **pricing,
        "message": f"Total savings: ${pricing['total_savings']:.2f}"
    }

def check_personalized_offers(customer_id: str):
    """
    Get personalized offers for a customer based on their profile.
    
    Args:
        customer_id: Customer identifier
    
    Returns:
        Dictionary with personalized offers
        Success: {
            "status": "success",
            "offers": [
                {
                    "title": "Birthday Bonus",
                    "description": "500 bonus points",
                    "type": "points",
                    "expires": "2025-12-31"
                }
            ]
        }
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT loyalty_tier, preferences
        FROM customers WHERE customer_id = ?
    """, (customer_id,))
    
    customer = cursor.fetchone()
    conn.close()
    
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    tier, preferences_json = customer
    preferences = json.loads(preferences_json)
    
    offers = []
    
    # Tier-based offers
    if tier in ["silver", "gold", "platinum"]:
        offers.append({
            "title": "Birthday Bonus",
            "description": "Earn 500 bonus points on your birthday",
            "type": "points",
            "value": 500,
            "expires": "On your birthday"
        })
    
    if tier == "platinum":
        offers.append({
            "title": "VIP Early Access",
            "description": "24-hour early access to new product launches",
            "type": "exclusive_access",
            "value": "N/A"
        })
    
    # Category-based offers
    favorite_categories = preferences.get("favorite_categories", [])
    if "Electronics" in favorite_categories:
        offers.append({
            "title": "Tech Lover Discount",
            "description": "Extra 10% off all electronics",
            "type": "discount",
            "value": 10,
            "category": "Electronics",
            "expires": (datetime.now().replace(day=1, month=datetime.now().month % 12 + 1)).strftime("%Y-%m-%d")
        })
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "offers": offers,
        "count": len(offers)
    }

print("✅ Loyalty and offers tools loaded")
