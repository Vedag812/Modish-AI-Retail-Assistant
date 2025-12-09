"""
Fulfillment Agent Tools - Firebase Firestore
Schedules delivery or reserve in-store slots, notifies logistics/store staff
"""
import json
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import STORE_LOCATIONS

def schedule_delivery(order_id: str, customer_address: dict, delivery_preference: str = "standard"):
    """
    Schedule home delivery for an order.
    
    Args:
        order_id: Order identifier
        customer_address: Delivery address details
        delivery_preference: "standard" (3-5 days), "express" (1-2 days), or "same_day"
    
    Returns:
        Dictionary with delivery schedule
        Success: {
            "status": "success",
            "order_id": "ORD123456",
            "delivery_type": "standard",
            "estimated_delivery": "2025-12-08",
            "tracking_number": "TRK987654321",
            "carrier": "FastShip Logistics"
        }
        Error: {"status": "error", "message": "..."}
    """
    delivery_times = {
        "same_day": (0, 0),  # Same day
        "express": (1, 2),   # 1-2 days
        "standard": (3, 5)   # 3-5 days
    }
    
    if delivery_preference not in delivery_times:
        return {
            "status": "error",
            "message": f"Invalid delivery preference. Choose from: {', '.join(delivery_times.keys())}"
        }
    
    min_days, max_days = delivery_times[delivery_preference]
    delivery_date = datetime.now() + timedelta(days=random.randint(min_days, max_days))
    
    tracking_number = f"TRK{random.randint(100000000, 999999999)}"
    carrier = random.choice(["FastShip Logistics", "QuickDeliver", "SpeedyPost", "Express Carriers"])
    
    return {
        "status": "success",
        "order_id": order_id,
        "delivery_type": delivery_preference,
        "estimated_delivery": delivery_date.strftime("%Y-%m-%d"),
        "estimated_time_window": "9 AM - 6 PM",
        "tracking_number": tracking_number,
        "carrier": carrier,
        "delivery_address": customer_address,
        "message": f"Delivery scheduled for {delivery_date.strftime('%B %d, %Y')}. Track your package with {tracking_number}"
    }

def schedule_store_pickup(order_id: str, store_location: str, customer_name: str):
    """
    Schedule in-store pickup for click & collect orders.
    
    Args:
        order_id: Order identifier
        store_location: Store location for pickup
        customer_name: Customer name for pickup verification
    
    Returns:
        Dictionary with pickup details
        Success: {
            "status": "success",
            "order_id": "ORD123456",
            "pickup_location": "New York - 5th Avenue",
            "ready_by": "2025-12-03T16:30:00",
            "pickup_code": "PKP4567",
            "store_hours": "9 AM - 9 PM"
        }
        Error: {"status": "error", "message": "..."}
    """
    if store_location not in STORE_LOCATIONS:
        return {
            "status": "error",
            "message": f"Invalid store location. Available: {', '.join(STORE_LOCATIONS)}"
        }
    
    # Ready in 2 hours
    ready_time = datetime.now() + timedelta(hours=2)
    pickup_code = f"PKP{random.randint(1000, 9999)}"
    
    return {
        "status": "success",
        "order_id": order_id,
        "pickup_location": store_location,
        "ready_by": ready_time.isoformat(),
        "ready_by_formatted": ready_time.strftime("%I:%M %p today"),
        "pickup_code": pickup_code,
        "customer_name": customer_name,
        "store_hours": "9 AM - 9 PM daily",
        "parking_info": "Free parking available",
        "message": f"Your order will be ready by {ready_time.strftime('%I:%M %p')}. Use pickup code {pickup_code} at the store."
    }

def notify_store_staff(order_id: str, store_location: str, order_items_json: str):
    """
    Notify store staff about a click & collect or in-store reservation order.
    
    Args:
        order_id: Order identifier
        store_location: Store location
        order_items_json: JSON string of items to prepare (e.g., '["SKU1001", "SKU1002"]')
    
    Returns:
        Dictionary with notification status
        Success: {
            "status": "success",
            "notification_sent": true,
            "staff_notified": ["John (Manager)", "Sarah (Sales Associate)"]
        }
    """
    try:
        order_items = json.loads(order_items_json) if order_items_json else []
    except:
        order_items = []
    
    staff_members = [
        f"{random.choice(['John', 'Sarah', 'Mike', 'Emily', 'David'])} ({random.choice(['Manager', 'Sales Associate', 'Inventory Specialist'])})"
        for _ in range(random.randint(2, 3))
    ]
    
    return {
        "status": "success",
        "order_id": order_id,
        "store_location": store_location,
        "notification_sent": True,
        "staff_notified": staff_members,
        "items_count": len(order_items),
        "priority": "standard",
        "timestamp": datetime.now().isoformat(),
        "message": f"Store staff at {store_location} have been notified to prepare your order."
    }

def track_shipment(tracking_number: str):
    """
    Track the status of a shipment.
    
    Args:
        tracking_number: Shipment tracking number
    
    Returns:
        Dictionary with tracking information
        Success: {
            "status": "success",
            "tracking_number": "TRK987654321",
            "current_status": "in_transit",
            "estimated_delivery": "2025-12-08",
            "tracking_events": [...]
        }
        Error: {"status": "error", "message": "Invalid tracking number"}
    """
    if not tracking_number.startswith("TRK"):
        return {
            "status": "error",
            "message": "Invalid tracking number format"
        }
    
    statuses = ["order_received", "processing", "shipped", "in_transit", "out_for_delivery", "delivered"]
    current_status = random.choice(statuses[:4])  # Don't show delivered yet for active orders
    
    # Generate tracking events
    events = []
    now = datetime.now()
    
    event_details = {
        "order_received": ("Order received by carrier", 48),
        "processing": ("Package processed at warehouse", 36),
        "shipped": ("Package shipped", 24),
        "in_transit": ("In transit to destination", 12),
        "out_for_delivery": ("Out for delivery", 2)
    }
    
    status_index = statuses.index(current_status)
    for i in range(status_index + 1):
        status_name = statuses[i]
        description, hours_ago = event_details.get(status_name, (status_name, 0))
        event_time = now - timedelta(hours=hours_ago)
        
        events.append({
            "status": status_name,
            "description": description,
            "location": random.choice(["Warehouse Hub", "Distribution Center", "Local Facility", "Delivery Station"]),
            "timestamp": event_time.isoformat(),
            "formatted_time": event_time.strftime("%b %d, %I:%M %p")
        })
    
    events.reverse()  # Most recent first
    
    return {
        "status": "success",
        "tracking_number": tracking_number,
        "current_status": current_status,
        "estimated_delivery": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "tracking_events": events,
        "carrier": "FastShip Logistics"
    }

def update_delivery_address(order_id: str, new_address: dict):
    """
    Update delivery address for an order (if not yet shipped).
    
    Args:
        order_id: Order identifier
        new_address: New delivery address
    
    Returns:
        Dictionary with update status
        Success: {
            "status": "success",
            "order_id": "ORD123456",
            "address_updated": true
        }
        Error: {"status": "error", "message": "Order already shipped"}
    """
    # Simulate checking if order can be modified
    can_modify = random.random() < 0.7  # 70% chance order can still be modified
    
    if can_modify:
        return {
            "status": "success",
            "order_id": order_id,
            "address_updated": True,
            "new_address": new_address,
            "message": "Delivery address updated successfully"
        }
    else:
        return {
            "status": "error",
            "message": "Cannot update address - order has already been shipped",
            "order_id": order_id
        }

print("✅ Fulfillment tools loaded (Firebase)")
