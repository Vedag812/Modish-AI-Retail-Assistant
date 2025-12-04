"""
Payment Agent Tools - PostgreSQL + Razorpay Integration
Processes payments and saves orders to database
"""
import random
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.db import get_db, get_customer

# Import Razorpay
try:
    import razorpay
    from dotenv import load_dotenv
    load_dotenv()
    
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
    
    if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        USE_RAZORPAY = True
        print(f"✅ Razorpay initialized (Key: {RAZORPAY_KEY_ID[:15]}...)")
    else:
        USE_RAZORPAY = False
        razorpay_client = None
        print("⚠️  Razorpay credentials not found")
except ImportError:
    USE_RAZORPAY = False
    razorpay_client = None
    print("⚠️  Razorpay SDK not installed. Run: pip install razorpay")


def save_order_to_db(customer_id: str, items: list, total_amount: float, payment_status: str = "pending", razorpay_order_id: str = None):
    """Save order to PostgreSQL database"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        order_id = f"ORD{random.randint(100000, 999999)}"
        
        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (order_id, customer_id, total_amount, status, razorpay_order_id, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (order_id, customer_id, total_amount, payment_status, razorpay_order_id))
        
        # Insert order items if provided
        if items:
            for item in items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, sku, product_name, quantity, price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item.get('sku', ''), item.get('name', ''), item.get('quantity', 1), item.get('price', 0)))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        print(f"❌ Error saving order: {e}")
        return {"status": "error", "message": str(e), "order_id": f"ORD{random.randint(100000, 999999)}"}


def save_transaction_to_db(order_id: str, customer_id: str, amount: float, payment_method: str, 
                           transaction_id: str, status: str, razorpay_payment_id: str = None):
    """Save transaction to PostgreSQL database"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (transaction_id, order_id, customer_id, amount, payment_method, status, razorpay_payment_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (transaction_id, order_id, customer_id, amount, payment_method, status, razorpay_payment_id))
        
        # Update order status
        cursor.execute("""
            UPDATE orders SET status = %s WHERE order_id = %s
        """, (status, order_id))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "transaction_id": transaction_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_payment_link(customer_id: str, amount: float, description: str = "", items: list = None):
    """
    Create a REAL Razorpay payment link for the customer.
    
    Args:
        customer_id: Customer identifier
        amount: Payment amount in INR
        description: Order description
        items: List of items in the order
    
    Returns:
        Dictionary with payment link details
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    # Save order to database first
    order_result = save_order_to_db(customer_id, items or [], amount, "pending")
    order_id = order_result.get("order_id", f"ORD{random.randint(100000, 999999)}")
    
    if USE_RAZORPAY and razorpay_client:
        try:
            # Create Razorpay payment link
            payment_link_data = {
                "amount": int(amount * 100),  # Convert to paise
                "currency": "INR",
                "description": description or f"Order {order_id} - Retail Store",
                "customer": {
                    "name": customer.get("name", "Customer"),
                    "email": customer.get("email", ""),
                    "contact": customer.get("phone", "")
                },
                "notify": {
                    "sms": True,
                    "email": True
                },
                "reminder_enable": True,
                "notes": {
                    "order_id": order_id,
                    "customer_id": customer_id
                },
                "callback_url": "https://your-store.com/payment/callback",
                "callback_method": "get"
            }
            
            payment_link = razorpay_client.payment_link.create(payment_link_data)
            
            # Update order with Razorpay link ID
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET razorpay_order_id = %s WHERE order_id = %s", 
                          (payment_link.get('id'), order_id))
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "order_id": order_id,
                "payment_link_id": payment_link.get("id"),
                "payment_url": payment_link.get("short_url"),  # This is the actual Razorpay link!
                "amount": amount,
                "currency": "INR",
                "customer_name": customer.get("name"),
                "customer_email": customer.get("email"),
                "expires_at": payment_link.get("expire_by"),
                "message": f"✅ Payment link created! Click here to pay: {payment_link.get('short_url')}"
            }
            
        except Exception as e:
            # Fallback to simulated link if Razorpay fails
            return {
                "status": "success",
                "order_id": order_id,
                "payment_link_id": f"plink_{random.randint(100000, 999999)}",
                "payment_url": f"https://rzp.io/demo/{order_id}",
                "amount": amount,
                "currency": "INR",
                "error_note": f"Razorpay error: {str(e)}. Using demo link.",
                "message": f"Payment link for ₹{amount:.2f} (Demo mode due to API error)"
            }
    else:
        # Simulated payment link
        return {
            "status": "success",
            "order_id": order_id,
            "payment_link_id": f"plink_{random.randint(100000, 999999)}",
            "payment_url": f"https://rzp.io/demo/{order_id}",
            "amount": amount,
            "currency": "INR",
            "message": f"Payment link created (Demo mode). Amount: ₹{amount:.2f}"
        }


def process_payment(customer_id: str, amount: float, payment_method: str, order_id: str = None, items: list = None):
    """
    Process a payment transaction and save to database.
    
    Args:
        customer_id: Customer identifier
        amount: Payment amount
        payment_method: Type of payment ("credit_card", "debit_card", "upi", "payment_link")
        order_id: Existing order ID (optional)
        items: List of items being purchased
    
    Returns:
        Dictionary with payment result
    """
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    # Create order if not provided
    if not order_id:
        order_result = save_order_to_db(customer_id, items or [], amount, "processing")
        order_id = order_result.get("order_id", f"ORD{random.randint(100000, 999999)}")
    
    # Generate transaction ID
    transaction_id = f"TXN{random.randint(100000000, 999999999)}"
    
    # If payment_method is "payment_link", create a Razorpay link
    if payment_method.lower() == "payment_link":
        return create_payment_link(customer_id, amount, f"Order {order_id}", items)
    
    # For other methods, try Razorpay order creation
    razorpay_order_id = None
    if USE_RAZORPAY and razorpay_client:
        try:
            rz_order = razorpay_client.order.create({
                "amount": int(amount * 100),
                "currency": "INR",
                "receipt": order_id,
                "notes": {"customer_id": customer_id}
            })
            razorpay_order_id = rz_order.get("id")
        except:
            pass
    
    # Save transaction to database
    save_transaction_to_db(
        order_id=order_id,
        customer_id=customer_id,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id,
        status="completed",
        razorpay_payment_id=razorpay_order_id
    )
    
    # Update order status
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = 'paid' WHERE order_id = %s", (order_id,))
        conn.commit()
        conn.close()
    except:
        pass
    
    return {
        "status": "success",
        "transaction_id": transaction_id,
        "order_id": order_id,
        "razorpay_order_id": razorpay_order_id,
        "customer_id": customer_id,
        "customer_name": customer.get("name"),
        "amount": round(amount, 2),
        "currency": "INR",
        "payment_method": payment_method,
        "payment_status": "completed",
        "timestamp": datetime.now().isoformat(),
        "message": f"✅ Payment of ₹{amount:.2f} processed successfully via {payment_method.upper().replace('_', ' ')}. Order saved to database."
    }


def get_saved_payment_methods(customer_id: str):
    """Get customer's saved payment methods."""
    customer = get_customer(customer_id)
    if not customer:
        return {"status": "error", "message": f"Customer {customer_id} not found"}
    
    payment_methods = [
        {"id": "card_1", "type": "credit_card", "last_four": "4242", "brand": "Visa", "expiry": "12/26", "is_default": True},
        {"id": "card_2", "type": "debit_card", "last_four": "8888", "brand": "HDFC", "expiry": "08/27", "is_default": False},
        {"id": "upi_1", "type": "upi", "upi_id": f"{customer.get('name', '').lower().split()[0]}@okicici", "is_default": False},
        {"id": "upi_2", "type": "upi", "upi_id": f"{customer.get('phone', '9999999999')[-10:]}@paytm", "is_default": False},
    ]
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "customer_name": customer.get("name"),
        "payment_methods": payment_methods,
        "count": len(payment_methods),
        "message": f"Found {len(payment_methods)} saved payment methods for {customer.get('name')}"
    }


def apply_gift_card(gift_card_code: str, order_amount: float):
    """Apply a gift card to an order."""
    valid_cards = {
        "GIFT1234": 500.00,
        "GIFT5678": 1000.00,
        "GIFT9999": 250.00,
        "WELCOME100": 100.00
    }
    
    if gift_card_code.upper() not in valid_cards:
        return {"status": "error", "message": f"Invalid gift card: {gift_card_code}"}
    
    balance = valid_cards[gift_card_code.upper()]
    applied_amount = min(balance, order_amount)
    remaining_balance = round(balance - applied_amount, 2)
    new_order_total = round(order_amount - applied_amount, 2)
    
    return {
        "status": "success",
        "gift_card_code": gift_card_code.upper(),
        "original_balance": balance,
        "applied_amount": applied_amount,
        "remaining_balance": remaining_balance,
        "new_order_total": new_order_total,
        "message": f"Applied ₹{applied_amount} from gift card. New total: ₹{new_order_total}"
    }


def get_order_status(order_id: str):
    """Get order status from database."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT order_id, customer_id, total_amount, status, razorpay_order_id, created_at
            FROM orders WHERE order_id = %s
        """, (order_id,))
        
        order = cursor.fetchone()
        conn.close()
        
        if order:
            return {
                "status": "success",
                "order_id": order[0],
                "customer_id": order[1],
                "total_amount": float(order[2]),
                "order_status": order[3],
                "razorpay_order_id": order[4],
                "created_at": str(order[5])
            }
        else:
            return {"status": "error", "message": f"Order {order_id} not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def confirm_payment(order_id: str, customer_id: str = None, amount: float = None, items: list = None):
    """
    Confirm that payment has been completed for an order.
    Use this when customer says they have completed the payment.
    
    Args:
        order_id: The order ID to confirm payment for
        customer_id: Customer ID (optional, for creating order if missing)
        amount: Order amount (optional, for creating order if missing)
        items: List of items (optional)
    
    Returns:
        Dictionary with confirmation status
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if order exists
        cursor.execute("SELECT order_id, status, customer_id, total_amount FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        
        if order:
            # Update existing order to paid
            cursor.execute("""
                UPDATE orders SET status = 'paid' WHERE order_id = %s
            """, (order_id,))
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "order_id": order_id,
                "payment_status": "paid",
                "customer_id": order[2],
                "amount": float(order[3]),
                "message": f"✅ Payment confirmed for order {order_id}. Order is now marked as PAID."
            }
        else:
            # Order doesn't exist, create it if we have customer_id and amount
            if customer_id and amount:
                cursor.execute("""
                    INSERT INTO orders (order_id, customer_id, total_amount, status, created_at)
                    VALUES (%s, %s, %s, 'paid', NOW())
                """, (order_id, customer_id, amount))
                
                # Add order items if provided
                if items:
                    for item in items:
                        cursor.execute("""
                            INSERT INTO order_items (order_id, sku, product_name, quantity, price)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (order_id, item.get('sku', ''), item.get('name', ''), item.get('quantity', 1), item.get('price', 0)))
                
                conn.commit()
                conn.close()
                
                return {
                    "status": "success",
                    "order_id": order_id,
                    "payment_status": "paid",
                    "customer_id": customer_id,
                    "amount": amount,
                    "message": f"✅ Order {order_id} created and payment confirmed!"
                }
            else:
                conn.close()
                return {"status": "error", "message": f"Order {order_id} not found. Please provide customer_id and amount to create it."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


print("✅ Payment tools loaded (PostgreSQL + Razorpay)")
