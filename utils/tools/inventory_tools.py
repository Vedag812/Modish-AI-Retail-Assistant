"""
Inventory Agent Tools - PostgreSQL Only
Real-time stock checking and fulfillment options
"""
import json
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.db import get_db, get_product, get_inventory

# Import real inventory API if available
try:
    from utils.external_apis.inventory_api import inventory_api
    USE_REAL_INVENTORY_API = True
    print("✅ Using REAL Inventory API integration")
except:
    USE_REAL_INVENTORY_API = False
    print("⚠️  Inventory API not available, using database")

def check_inventory(sku: str, location: str = None):
    """
    Check inventory levels for a product across locations.
    
    Args:
        sku: Product SKU to check
        location: Optional specific location to check
    
    Returns:
        Dictionary with inventory status
    """
    product = get_product(sku)
    if not product:
        return {"status": "error", "message": f"Product {sku} not found"}
    
    inventory = get_inventory(sku, location)
    
    if not inventory:
        return {
            "status": "success",
            "sku": sku,
            "product_name": product["name"],
            "inventory": [],
            "message": "Product not available at any location"
        }
    
    total_stock = sum(item["quantity"] for item in inventory)
    
    return {
        "status": "success",
        "sku": sku,
        "product_name": product["name"],
        "total_stock": total_stock,
        "inventory": inventory,
        "in_stock": total_stock > 0
    }

def get_fulfillment_options(sku: str, customer_location: str = ""):
    """
    Get available fulfillment options for a product.
    
    Args:
        sku: Product SKU
        customer_location: Customer's location for shipping estimates
    
    Returns:
        Dictionary with fulfillment options
    """
    product = get_product(sku)
    if not product:
        return {"status": "error", "message": f"Product {sku} not found"}
    
    inventory = get_inventory(sku)
    available_locations = [item for item in inventory if item["quantity"] > 0]
    
    fulfillment_options = []
    
    # Standard shipping (free above ₹500)
    fulfillment_options.append({
        "type": "standard_shipping",
        "name": "Standard Shipping",
        "cost": 49 if product["price"] < 500 else 0,
        "cost_display": "₹49" if product["price"] < 500 else "FREE",
        "estimated_days": "5-7 business days",
        "available": len(available_locations) > 0
    })
    
    # Express shipping
    fulfillment_options.append({
        "type": "express_shipping",
        "name": "Express Shipping",
        "cost": 99,
        "cost_display": "₹99",
        "estimated_days": "2-3 business days",
        "available": len(available_locations) > 0
    })
    
    # Same day delivery
    fulfillment_options.append({
        "type": "same_day",
        "name": "Same Day Delivery",
        "cost": 149,
        "cost_display": "₹149",
        "estimated_days": "Today (order before 2 PM)",
        "available": len(available_locations) > 0
    })
    
    # Store pickup
    for loc in available_locations[:3]:
        fulfillment_options.append({
            "type": "store_pickup",
            "name": f"Store Pickup - {loc['location']}",
            "cost": 0,
            "estimated_days": "Same day",
            "available": True,
            "location": loc["location"],
            "stock": loc["quantity"]
        })
    
    return {
        "status": "success",
        "sku": sku,
        "product_name": product["name"],
        "fulfillment_options": fulfillment_options,
        "total_available_stock": sum(item["quantity"] for item in available_locations)
    }

def reserve_inventory(sku: str, quantity: int, location: str):
    """
    Reserve inventory for a customer (simulated).
    """
    product = get_product(sku)
    if not product:
        return {"status": "error", "message": f"Product {sku} not found"}
    
    inventory = get_inventory(sku, location)
    if not inventory or inventory[0]["quantity"] < quantity:
        return {
            "status": "error",
            "message": f"Insufficient stock at {location}"
        }
    
    # In production, would actually reserve in database
    reservation_id = f"RES{random.randint(100000, 999999)}"
    
    return {
        "status": "success",
        "reservation_id": reservation_id,
        "sku": sku,
        "quantity": quantity,
        "location": location,
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        "message": f"Reserved {quantity} unit(s) of {product['name']} at {location}"
    }

print("✅ Inventory tools loaded (PostgreSQL)")
