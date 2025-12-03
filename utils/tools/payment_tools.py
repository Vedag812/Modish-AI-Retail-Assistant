"""
Payment Agent Tools
Processes payments via saved cards, UPI, gift cards, or in-store POS
Now with REAL API integration!
"""
import sqlite3
import json
import random
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DB_PATH

# Import real payment API
try:
    from utils.external_apis.payment_api import payment_api
    USE_REAL_PAYMENT_API = True
    print("✅ Using REAL Payment API integration")
except:
    USE_REAL_PAYMENT_API = False
    print("⚠️  Payment API not available, using simulation")

def process_payment(customer_id: str, amount: float, payment_method: str, payment_details: str = ""):
    """
    Process a payment transaction.
    
    Args:
        customer_id: Customer identifier
        amount: Payment amount
        payment_method: Type of payment ("credit_card", "upi", "gift_card", "in_store_pos")
        payment_details: Additional payment details as string (e.g., "card ending in 4242", "UPI ID: user@bank")
    
    Returns:
        Dictionary with payment result
        Success: {
            "status": "success",
            "transaction_id": "TXN123456789",
            "amount": 129.99,
            "payment_method": "credit_card",
            "payment_status": "completed",
            "timestamp": "2025-12-03T14:30:00"
        }
        Error: {"status": "error", "message": "Payment declined"}
    """
    # Use REAL Payment API if available
    if USE_REAL_PAYMENT_API:
        try:
            # Create payment order via real API
            order_result = payment_api.create_payment_order(
                amount=amount,
                currency="USD",
                customer_id=customer_id
            )
            
            if order_result["status"] == "success":
                # Simulate payment verification
                payment_id = f"PAY_{random.randint(100000000, 999999999)}"
                verification = payment_api.verify_payment(
                    order_id=order_result["order_id"],
                    payment_id=payment_id
                )
                
                if verification.get("verified", False):
                    return {
                        "status": "success",
                        "transaction_id": verification.get("transaction_id", payment_id),
                        "order_id": order_result["order_id"],
                        "customer_id": customer_id,
                        "amount": round(amount, 2),
                        "payment_method": payment_method,
                        "payment_status": "completed",
                        "timestamp": datetime.now().isoformat(),
                        "provider": order_result.get("provider", "payment_api"),
                        "message": f"Payment of ${amount:.2f} processed successfully via {order_result.get('provider', 'API')}"
                    }
            
            return {
                "status": "error",
                "message": order_result.get("message", "Payment API error")
            }
        except Exception as e:
            print(f"Payment API error: {e}, falling back to simulation")
    
    # Fallback: Simulate payment processing
    success_rate = 0.95
    
    if random.random() < success_rate:
        transaction_id = f"TXN{random.randint(100000000, 999999999)}"
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "amount": round(amount, 2),
            "payment_method": payment_method,
            "payment_status": "completed",
            "timestamp": datetime.now().isoformat(),
            "message": f"Payment of ${amount:.2f} processed successfully (simulated)"
        }
    else:
        return {
            "status": "error",
            "message": "Payment declined. Please try another payment method.",
            "error_code": random.choice(["INSUFFICIENT_FUNDS", "CARD_DECLINED", "NETWORK_ERROR"])
        }

def get_saved_payment_methods(customer_id: str):
    """
    Get customer's saved payment methods.
    
    Args:
        customer_id: Customer identifier
    
    Returns:
        Dictionary with saved payment methods
        Success: {
            "status": "success",
            "payment_methods": [
                {
                    "id": "card_1",
                    "type": "credit_card",
                    "last_four": "4242",
                    "brand": "Visa",
                    "is_default": true
                },
                {
                    "id": "upi_1",
                    "type": "upi",
                    "upi_id": "customer@bank",
                    "is_default": false
                }
            ]
        }
        Error: {"status": "error", "message": "Customer not found"}
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?", (customer_id,))
    if not cursor.fetchone():
        conn.close()
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    conn.close()
    
    # Simulated saved payment methods
    payment_methods = [
        {
            "id": "card_1",
            "type": "credit_card",
            "last_four": "4242",
            "brand": "Visa",
            "expiry": "12/26",
            "is_default": True
        },
        {
            "id": "card_2",
            "type": "credit_card",
            "last_four": "8888",
            "brand": "Mastercard",
            "expiry": "08/27",
            "is_default": False
        },
        {
            "id": "upi_1",
            "type": "upi",
            "upi_id": f"{customer_id.lower()}@okbank",
            "is_default": False
        }
    ]
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "payment_methods": payment_methods,
        "count": len(payment_methods)
    }

def apply_gift_card(gift_card_code: str, order_amount: float):
    """
    Apply a gift card to an order.
    
    Args:
        gift_card_code: Gift card code
        order_amount: Total order amount
    
    Returns:
        Dictionary with gift card application result
        Success: {
            "status": "success",
            "gift_card_code": "GIFT1234",
            "balance": 50.00,
            "applied_amount": 50.00,
            "remaining_balance": 0,
            "new_order_total": 79.99
        }
        Error: {"status": "error", "message": "Invalid gift card"}
    """
    # Simulated gift card validation
    valid_cards = {
        "GIFT1234": 50.00,
        "GIFT5678": 100.00,
        "GIFT9999": 25.00
    }
    
    if gift_card_code not in valid_cards:
        return {
            "status": "error",
            "message": "Invalid or expired gift card code"
        }
    
    balance = valid_cards[gift_card_code]
    applied = min(balance, order_amount)
    remaining_balance = balance - applied
    new_total = max(0, order_amount - applied)
    
    return {
        "status": "success",
        "gift_card_code": gift_card_code,
        "original_balance": balance,
        "applied_amount": round(applied, 2),
        "remaining_balance": round(remaining_balance, 2),
        "new_order_total": round(new_total, 2),
        "message": f"Gift card applied. ${applied:.2f} deducted from your order."
    }

def handle_payment_retry(transaction_id: str):
    """
    Retry a failed payment transaction.
    
    Args:
        transaction_id: Original transaction ID
    
    Returns:
        Dictionary with retry result
        Success: {
            "status": "success",
            "transaction_id": "TXN987654321",
            "retry_status": "completed"
        }
        Error: {"status": "error", "message": "Retry failed"}
    """
    # Simulate retry with higher success rate
    if random.random() < 0.85:
        new_transaction_id = f"TXN{random.randint(100000000, 999999999)}"
        return {
            "status": "success",
            "original_transaction_id": transaction_id,
            "new_transaction_id": new_transaction_id,
            "retry_status": "completed",
            "timestamp": datetime.now().isoformat(),
            "message": "Payment retry successful"
        }
    else:
        return {
            "status": "error",
            "message": "Payment retry failed. Please contact support or try a different payment method.",
            "support_contact": "1-800-SUPPORT"
        }

def calculate_split_payment(total_amount: float, payment_methods_json: str):
    """
    Calculate split payment across multiple methods.
    
    Args:
        total_amount: Total order amount
        payment_methods_json: JSON string of payment methods with amounts
            Example: '[{"method": "gift_card", "amount": 50}, {"method": "credit_card", "amount": 79.99}]'
    
    Returns:
        Dictionary with split payment breakdown
        Success: {
            "status": "success",
            "total_amount": 129.99,
            "breakdown": [...]
        }
        Error: {"status": "error", "message": "Split amounts don't match total"}
    """
    try:
        payment_methods = json.loads(payment_methods_json)
    except:
        return {"status": "error", "message": "Invalid payment methods format"}
    
    total_split = sum(pm['amount'] for pm in payment_methods)
    
    if abs(total_split - total_amount) > 0.01:  # Allow for rounding
        return {
            "status": "error",
            "message": f"Split payment amounts (${total_split:.2f}) don't match order total (${total_amount:.2f})"
        }
    
    return {
        "status": "success",
        "total_amount": round(total_amount, 2),
        "breakdown": payment_methods,
        "payment_count": len(payment_methods),
        "message": f"Order will be split across {len(payment_methods)} payment methods"
    }

print("✅ Payment tools loaded")
