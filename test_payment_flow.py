"""Quick test of payment flow"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.tools.payment_tools import create_payment_link, confirm_payment, get_order_status

print("\n" + "="*60)
print("🧪 PAYMENT FLOW TEST")
print("="*60)

# Step 1: Create payment link
print("\n📍 Step 1: Creating payment link...")
result = create_payment_link(
    customer_id="CUST2031",
    amount=299.99,
    description="Test Order - Organic Honey",
    items=[{"sku": "IND1090", "name": "Organic Honey", "quantity": 1, "price": 299.99}]
)

print(f"  Status: {result['status']}")
print(f"  📦 ORDER_ID: {result.get('order_id')}")
print(f"  💳 Payment Link: {result.get('payment_url')}")

order_id = result.get('order_id')

# Step 2: Check order status (before payment)
print(f"\n📍 Step 2: Checking order status...")
status = get_order_status(order_id)
print(f"  Order {order_id}: Status = {status.get('order_status', 'N/A').upper()}")

# Step 3: Confirm payment
print(f"\n📍 Step 3: Confirming payment...")
confirm = confirm_payment(order_id)
print(f"  {confirm.get('message')}")

# Step 4: Check order status (after payment)
print(f"\n📍 Step 4: Verifying order status after confirmation...")
status = get_order_status(order_id)
print(f"  Order {order_id}: Status = {status.get('order_status', 'N/A').upper()}")

print("\n" + "="*60)
print("✅ Payment flow test complete!")
print("="*60 + "\n")
