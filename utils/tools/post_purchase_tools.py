"""
Post-Purchase Support Tools - Firebase Firestore
Handles returns, exchanges, reviews, and order history
"""
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.db import get_customer, get_product

def initiate_return(customer_id: str, order_id: str, sku: str, reason: str):
    """
    Initiate a product return.
    
    Args:
        customer_id: Customer identifier
        order_id: Order identifier
        sku: Product SKU to return
        reason: Reason for return
    
    Returns:
        Dictionary with return details
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    product = get_product(sku)
    if not product:
        return {"status": "error", "message": f"Product {sku} not found"}
    
    return_id = f"RET{random.randint(100000, 999999)}"
    
    return {
        "status": "success",
        "return_id": return_id,
        "customer_id": customer_id,
        "order_id": order_id,
        "sku": sku,
        "product_name": product["name"],
        "reason": reason,
        "return_status": "initiated",
        "refund_amount": product["price"],
        "return_label_url": f"https://returns.example.com/label/{return_id}",
        "instructions": [
            "Print the return label from the URL above",
            "Pack the item securely in original packaging",
            "Drop off at any UPS location",
            "Refund will be processed within 3-5 business days"
        ],
        "message": f"Return initiated for {product['name']}. Return ID: {return_id}"
    }

def request_exchange(customer_id: str, order_id: str, sku: str, new_sku: str, reason: str):
    """
    Request a product exchange.
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    product = get_product(sku)
    new_product = get_product(new_sku)
    
    if not product:
        return {"status": "error", "message": f"Original product {sku} not found"}
    if not new_product:
        return {"status": "error", "message": f"New product {new_sku} not found"}
    
    exchange_id = f"EXC{random.randint(100000, 999999)}"
    price_diff = round(new_product["price"] - product["price"], 2)
    
    return {
        "status": "success",
        "exchange_id": exchange_id,
        "customer_id": customer_id,
        "original_product": {"sku": sku, "name": product["name"], "price": product["price"]},
        "new_product": {"sku": new_sku, "name": new_product["name"], "price": new_product["price"]},
        "price_difference": price_diff,
        "action_required": "Pay additional" if price_diff > 0 else "Refund to be issued" if price_diff < 0 else "No additional payment",
        "message": f"Exchange initiated. Swapping {product['name']} for {new_product['name']}"
    }

def submit_review(customer_id: str, sku: str, rating: int, review_text: str):
    """
    Submit a product review.
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    product = get_product(sku)
    if not product:
        return {"status": "error", "message": f"Product {sku} not found"}
    
    if rating < 1 or rating > 5:
        return {"status": "error", "message": "Rating must be between 1 and 5"}
    
    review_id = f"REV{random.randint(100000, 999999)}"
    
    # Award points for review
    points_earned = 25
    
    return {
        "status": "success",
        "review_id": review_id,
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "sku": sku,
        "product_name": product["name"],
        "rating": rating,
        "review_text": review_text,
        "points_earned": points_earned,
        "submitted_at": datetime.now().isoformat(),
        "message": f"Thank you for your review! You earned {points_earned} loyalty points."
    }

def get_order_history(customer_id: str, limit: int = 10):
    """
    Get customer's order history.
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    purchase_history = customer.get("purchase_history", [])
    
    # Generate sample orders if history is empty
    if not purchase_history:
        purchase_history = [
            {
                "order_id": f"ORD{random.randint(100000, 999999)}",
                "sku": "ELEC1006",
                "name": "Sony WH-1000XM5 Headphones",
                "amount": 399.99,
                "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "delivered"
            }
        ]
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "total_orders": len(purchase_history),
        "orders": purchase_history[:limit],
        "message": f"Found {len(purchase_history)} orders for {customer['name']}"
    }

def track_return(return_id: str):
    """
    Track return status.
    """
    # Simulated tracking
    statuses = ["initiated", "label_created", "in_transit", "received", "inspecting", "refund_processed"]
    current_status = random.choice(statuses)
    
    return {
        "status": "success",
        "return_id": return_id,
        "return_status": current_status,
        "estimated_refund_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "tracking_number": f"1Z{random.randint(100000000, 999999999)}",
        "message": f"Return {return_id} is currently: {current_status.replace('_', ' ').title()}"
    }

print("✅ Post-purchase support tools loaded (Firebase)")
