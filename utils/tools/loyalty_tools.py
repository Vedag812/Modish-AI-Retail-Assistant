"""
Loyalty Agent Tools - PostgreSQL Only
Handles loyalty points, tiers, discounts, and offers
"""
import json
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.db import get_db, get_customer, update_customer_points, update_customer_tier, get_promotions, create_customer, generate_customer_id

# Tier benefits configuration
TIER_BENEFITS = {
    "bronze": {"discount": 0, "free_shipping_min": 100, "points_multiplier": 1},
    "silver": {"discount": 5, "free_shipping_min": 75, "points_multiplier": 1.25},
    "gold": {"discount": 10, "free_shipping_min": 50, "points_multiplier": 1.5},
    "platinum": {"discount": 20, "free_shipping_min": 0, "points_multiplier": 2}
}

def get_loyalty_status(customer_id: str):
    """
    Get customer's loyalty tier, points, and benefits.
    
    Args:
        customer_id: Customer identifier
    
    Returns:
        Dictionary with loyalty status and benefits
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    tier = customer["loyalty_tier"].lower()
    points = customer["loyalty_points"]
    benefits = TIER_BENEFITS.get(tier, TIER_BENEFITS["bronze"])
    
    # Calculate points to next tier
    tier_thresholds = {"bronze": 500, "silver": 1500, "gold": 3000, "platinum": float('inf')}
    tier_order = ["bronze", "silver", "gold", "platinum"]
    current_idx = tier_order.index(tier)
    
    next_tier = None
    points_to_next = 0
    if current_idx < len(tier_order) - 1:
        next_tier = tier_order[current_idx + 1]
        points_to_next = tier_thresholds[tier] - points
        if points_to_next < 0:
            points_to_next = 0
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "loyalty_tier": customer["loyalty_tier"],
        "loyalty_points": points,
        "tier_discount": benefits["discount"],
        "free_shipping_minimum": benefits["free_shipping_min"],
        "points_multiplier": benefits["points_multiplier"],
        "next_tier": next_tier.capitalize() if next_tier else None,
        "points_to_next_tier": points_to_next,
        "benefits_summary": f"{benefits['discount']}% discount, free shipping on orders ${benefits['free_shipping_min']}+"
    }

def apply_promotion(promo_code: str, order_total: float, customer_id: str = None):
    """
    Validate and apply a promotion code.
    """
    promotions = get_promotions()
    promo = None
    for p in promotions:
        if p["code"].upper() == promo_code.upper():
            promo = p
            break
    
    if not promo:
        return {"status": "error", "message": f"Invalid promo code: {promo_code}"}
    
    if order_total < promo["min_order"]:
        return {
            "status": "error",
            "message": f"Minimum order of ${promo['min_order']} required for {promo_code}"
        }
    
    discount_amount = round(order_total * (promo["discount_percent"] / 100), 2)
    new_total = round(order_total - discount_amount, 2)
    
    return {
        "status": "success",
        "promo_code": promo_code,
        "description": promo["description"],
        "original_total": order_total,
        "discount_percent": promo["discount_percent"],
        "discount_amount": discount_amount,
        "new_total": new_total,
        "message": f"Promo {promo_code} applied! You saved ${discount_amount}"
    }

def calculate_final_price(customer_id: str, base_price: float, promo_code: str = None):
    """
    Calculate final price with loyalty discount and optional promo code.
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    tier = customer["loyalty_tier"].lower()
    benefits = TIER_BENEFITS.get(tier, TIER_BENEFITS["bronze"])
    
    # Apply tier discount
    tier_discount = round(base_price * (benefits["discount"] / 100), 2)
    price_after_tier = round(base_price - tier_discount, 2)
    
    # Apply promo code if provided
    promo_discount = 0
    promo_info = None
    if promo_code:
        promo_result = apply_promotion(promo_code, price_after_tier, customer_id)
        if promo_result["status"] == "success":
            promo_discount = promo_result["discount_amount"]
            price_after_tier = promo_result["new_total"]
            promo_info = promo_result
    
    # Determine shipping
    shipping_cost = 0 if price_after_tier >= benefits["free_shipping_min"] or benefits["free_shipping_min"] == 0 else 5.99
    
    final_price = round(price_after_tier + shipping_cost, 2)
    
    # Calculate points earned
    points_earned = int(base_price * benefits["points_multiplier"])
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "loyalty_tier": customer["loyalty_tier"],
        "base_price": base_price,
        "tier_discount": tier_discount,
        "tier_discount_percent": benefits["discount"],
        "promo_discount": promo_discount,
        "shipping_cost": shipping_cost,
        "final_price": final_price,
        "points_earned": points_earned,
        "savings_total": round(tier_discount + promo_discount, 2),
        "promo_applied": promo_info
    }

def register_new_customer(name: str, email: str, phone: str = "", location: str = ""):
    """
    Register a new customer in the database.
    
    Args:
        name: Customer's full name
        email: Customer's email address
        phone: Customer's phone number (optional)
        location: Customer's location (optional)
    
    Returns:
        Dictionary with new customer details
    """
    customer_id = generate_customer_id()
    result = create_customer(customer_id, name, email, phone, location, "Bronze", 100)
    
    if result["status"] == "success":
        return {
            "status": "success",
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "loyalty_tier": "Bronze",
            "loyalty_points": 100,
            "message": f"Welcome {name}! Your customer ID is {customer_id}. You start with Bronze tier and 100 bonus points!"
        }
    return result

def add_loyalty_points(customer_id: str, points: int, reason: str = "Purchase"):
    """
    Add loyalty points to a customer's account.
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    update_customer_points(customer_id, points)
    
    new_points = customer["loyalty_points"] + points
    
    # Check for tier upgrade
    tier_thresholds = {"Bronze": 0, "Silver": 500, "Gold": 1500, "Platinum": 3000}
    current_tier = customer["loyalty_tier"]
    new_tier = current_tier
    
    for tier, threshold in sorted(tier_thresholds.items(), key=lambda x: x[1], reverse=True):
        if new_points >= threshold:
            new_tier = tier
            break
    
    if new_tier != current_tier:
        update_customer_tier(customer_id, new_tier)
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "points_added": points,
        "reason": reason,
        "new_total": new_points,
        "tier_upgraded": new_tier != current_tier,
        "new_tier": new_tier if new_tier != current_tier else None,
        "message": f"Added {points} points for {reason}. New balance: {new_points}"
    }

print("✅ Loyalty and offers tools loaded (PostgreSQL)")
