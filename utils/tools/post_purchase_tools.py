"""
Post-Purchase Support Agent Tools
Handles returns/exchanges, tracks shipments, and solicits feedback
"""
import sqlite3
import json
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DB_PATH

def initiate_return(order_id: str, items_to_return_json: str, reason: str):
    """
    Initiate a return or exchange for order items.
    
    Args:
        order_id: Order identifier
        items_to_return_json: JSON string of items to return with quantities
            Example: '[{"sku": "SKU1001", "quantity": 1, "reason": "damaged"}]'
        reason: Overall return reason
    
    Returns:
        Dictionary with return authorization
        Success: {
            "status": "success",
            "return_id": "RET123456",
            "order_id": "ORD123456",
            "items": [...],
            "refund_amount": 129.99,
            "return_label_url": "https://...",
            "return_deadline": "2025-12-30"
        }
        Error: {"status": "error", "message": "..."}
    """
    # Parse JSON items
    try:
        items_to_return = json.loads(items_to_return_json) if items_to_return_json else []
    except:
        items_to_return = []
    
    # Check if order exists (simplified)
    return_id = f"RET{random.randint(100000, 999999)}"
    
    # Calculate refund amount (simplified - would normally check actual order)
    refund_amount = sum(100.0 for item in items_to_return)  # Placeholder
    
    # Generate return label
    return_label_url = f"https://returns.example.com/label/{return_id}"
    
    # Return deadline (30 days from now)
    deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    return {
        "status": "success",
        "return_id": return_id,
        "order_id": order_id,
        "items_to_return": items_to_return,
        "reason": reason,
        "refund_amount": round(refund_amount, 2),
        "refund_method": "original_payment_method",
        "return_label_url": return_label_url,
        "return_deadline": deadline,
        "instructions": "Print the return label and drop off at any shipping location",
        "message": f"Return request {return_id} created. You have until {deadline} to return the items."
    }

def process_exchange(order_id: str, original_sku: str, exchange_sku: str, reason: str):
    """
    Process an exchange for a different product or size.
    
    Args:
        order_id: Original order identifier
        original_sku: SKU of item to return
        exchange_sku: SKU of item to receive
        reason: Reason for exchange
    
    Returns:
        Dictionary with exchange details
        Success: {
            "status": "success",
            "exchange_id": "EXC123456",
            "original_item": {...},
            "exchange_item": {...},
            "price_difference": 10.00
        }
        Error: {"status": "error", "message": "..."}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get both products
    cursor.execute("SELECT sku, name, current_price FROM products WHERE sku IN (?, ?)", 
                   (original_sku, exchange_sku))
    products = cursor.fetchall()
    conn.close()
    
    if len(products) != 2:
        return {
            "status": "error",
            "message": "One or both products not found"
        }
    
    original = next(p for p in products if p[0] == original_sku)
    exchange = next(p for p in products if p[0] == exchange_sku)
    
    price_difference = exchange[2] - original[2]
    exchange_id = f"EXC{random.randint(100000, 999999)}"
    
    result = {
        "status": "success",
        "exchange_id": exchange_id,
        "order_id": order_id,
        "original_item": {
            "sku": original[0],
            "name": original[1],
            "price": original[2]
        },
        "exchange_item": {
            "sku": exchange[0],
            "name": exchange[1],
            "price": exchange[2]
        },
        "price_difference": round(price_difference, 2),
        "reason": reason
    }
    
    if price_difference > 0:
        result["message"] = f"Exchange approved. You will be charged ${price_difference:.2f} for the price difference."
        result["additional_payment_required"] = True
    elif price_difference < 0:
        result["message"] = f"Exchange approved. You will receive a refund of ${abs(price_difference):.2f}."
        result["refund_amount"] = abs(price_difference)
    else:
        result["message"] = "Exchange approved. No price difference."
    
    result["shipping_label_url"] = f"https://exchange.example.com/label/{exchange_id}"
    
    return result

def track_return_status(return_id: str):
    """
    Track the status of a return request.
    
    Args:
        return_id: Return request identifier
    
    Returns:
        Dictionary with return tracking information
        Success: {
            "status": "success",
            "return_id": "RET123456",
            "current_status": "received",
            "refund_status": "processing",
            "estimated_refund_date": "2025-12-10"
        }
    """
    if not return_id.startswith("RET"):
        return {
            "status": "error",
            "message": "Invalid return ID format"
        }
    
    statuses = [
        "requested",
        "label_generated",
        "in_transit",
        "received",
        "inspecting",
        "approved",
        "refund_processed"
    ]
    
    current_status = random.choice(statuses[1:5])  # Simulate active return
    status_index = statuses.index(current_status)
    
    # Generate timeline
    timeline = []
    now = datetime.now()
    
    for i in range(status_index + 1):
        event_time = now - timedelta(days=(status_index - i) * 2)
        timeline.append({
            "status": statuses[i],
            "timestamp": event_time.isoformat(),
            "formatted_time": event_time.strftime("%b %d, %Y")
        })
    
    # Determine refund status
    refund_status = "not_started"
    estimated_refund_date = None
    
    if current_status in ["approved", "refund_processed"]:
        refund_status = "processing" if current_status == "approved" else "completed"
        estimated_refund_date = (now + timedelta(days=3)).strftime("%Y-%m-%d")
    
    return {
        "status": "success",
        "return_id": return_id,
        "current_status": current_status,
        "refund_status": refund_status,
        "estimated_refund_date": estimated_refund_date,
        "timeline": timeline,
        "message": f"Return is currently: {current_status.replace('_', ' ').title()}"
    }

def submit_product_review(customer_id: str, sku: str, rating: int, review_text: str = ""):
    """
    Submit a product review and rating.
    
    Args:
        customer_id: Customer identifier
        sku: Product SKU
        rating: Rating from 1-5 stars
        review_text: Optional review text
    
    Returns:
        Dictionary with review submission result
        Success: {
            "status": "success",
            "review_id": "REV123456",
            "points_earned": 50
        }
        Error: {"status": "error", "message": "..."}
    """
    if rating < 1 or rating > 5:
        return {
            "status": "error",
            "message": "Rating must be between 1 and 5 stars"
        }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verify product exists
    cursor.execute("SELECT name FROM products WHERE sku = ?", (sku,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return {
            "status": "error",
            "message": f"Product {sku} not found"
        }
    
    # Verify customer exists
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?", (customer_id,))
    if not cursor.fetchone():
        conn.close()
        return {
            "status": "error",
            "message": f"Customer {customer_id} not found"
        }
    
    conn.close()
    
    review_id = f"REV{random.randint(100000, 999999)}"
    points_earned = 50  # Reward points for leaving a review
    
    return {
        "status": "success",
        "review_id": review_id,
        "customer_id": customer_id,
        "sku": sku,
        "product_name": product[0],
        "rating": rating,
        "review_text": review_text,
        "points_earned": points_earned,
        "message": f"Thank you for your review! You earned {points_earned} loyalty points."
    }

def request_order_modification(order_id: str, modification_type: str, details: dict):
    """
    Request modification to an existing order (if not yet shipped).
    
    Args:
        order_id: Order identifier
        modification_type: Type of modification ("cancel", "change_item", "change_quantity", "change_address")
        details: Modification details
    
    Returns:
        Dictionary with modification result
        Success: {
            "status": "success",
            "modification_allowed": true,
            "message": "Order modification successful"
        }
        Error: {"status": "error", "message": "Order already shipped"}
    """
    # Simulate checking if modification is allowed
    can_modify = random.random() < 0.65  # 65% chance order can be modified
    
    if not can_modify:
        return {
            "status": "error",
            "message": "Order has already been shipped and cannot be modified. Please initiate a return after delivery.",
            "order_id": order_id
        }
    
    modification_id = f"MOD{random.randint(100000, 999999)}"
    
    messages = {
        "cancel": "Order has been successfully cancelled. Refund will be processed within 3-5 business days.",
        "change_item": "Order items have been updated successfully.",
        "change_quantity": "Order quantity has been updated successfully.",
        "change_address": "Delivery address has been updated successfully."
    }
    
    return {
        "status": "success",
        "modification_id": modification_id,
        "order_id": order_id,
        "modification_type": modification_type,
        "modification_allowed": True,
        "details": details,
        "message": messages.get(modification_type, "Order modified successfully")
    }

def get_order_history(customer_id: str, limit: int = 10):
    """
    Get customer's order history.
    
    Args:
        customer_id: Customer identifier
        limit: Maximum number of orders to return
    
    Returns:
        Dictionary with order history
        Success: {
            "status": "success",
            "orders": [
                {
                    "order_id": "ORD123456",
                    "date": "2025-11-15",
                    "total": 129.99,
                    "status": "delivered"
                }
            ]
        }
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT order_id, total, payment_status, fulfillment_status, created_at
        FROM orders
        WHERE customer_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (customer_id, limit))
    
    orders = []
    for row in cursor.fetchall():
        orders.append({
            "order_id": row[0],
            "total": row[1],
            "payment_status": row[2],
            "fulfillment_status": row[3],
            "order_date": row[4].split('T')[0] if row[4] else "N/A"
        })
    
    conn.close()
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "orders": orders,
        "count": len(orders)
    }

print("✅ Post-purchase support tools loaded")
