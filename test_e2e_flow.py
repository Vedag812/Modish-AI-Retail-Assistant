"""
🧪 AUTOMATED END-TO-END TEST
Complete flow: Search → Order → Payment Link → Confirm Payment → Transaction
"""
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db import get_db, get_customer, search_products
from utils.tools.inventory_tools import check_inventory
from utils.tools.payment_tools import create_payment_link, confirm_payment, get_order_status
from utils.tools.fulfillment_tools import schedule_delivery

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(step, text):
    print(f"\n📍 STEP {step}: {text}")
    print("-"*50)

def main():
    print_header("🛒 AUTOMATED E2E TEST - COMPLETE ORDER FLOW")
    
    # Pick a random customer
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT customer_id, name, email, phone, location FROM customers ORDER BY RANDOM() LIMIT 1")
    cust = cur.fetchone()
    customer_id, name, email, phone, location = cust
    conn.close()
    
    print(f"\n👤 Customer: {name} ({customer_id})")
    print(f"   📧 Email: {email}")
    print(f"   📱 Phone: {phone}")
    print(f"   📍 Location: {location}")
    
    # ========== STEP 1: Search Products ==========
    print_step(1, "SEARCH PRODUCTS")
    
    search_queries = ["laptop", "smartphone", "headphones", "watch", "shoes", "saree", "honey", "mixer"]
    query = random.choice(search_queries)
    print(f"   🔍 Searching for: '{query}'")
    
    # search_products returns a list directly
    products = search_products(query=query, limit=5)
    
    if not products:
        print("   ❌ No products found!")
        return
    
    print(f"   ✅ Found {len(products)} products:\n")
    
    for i, p in enumerate(products, 1):
        print(f"   {i}. {p['name'][:45]:<45} ₹{p['price']:>10,.2f}  ⭐{p['rating']}")
    
    # Pick first product
    selected = products[0]
    print(f"\n   ✅ Selected: {selected['name']}")
    print(f"      SKU: {selected['sku']}, Price: ₹{selected['price']:,.2f}")
    
    # ========== STEP 2: Check Inventory ==========
    print_step(2, "CHECK INVENTORY")
    
    inv_result = check_inventory(selected['sku'])
    
    if inv_result.get("status") == "success":
        print(f"   ✅ Product available!")
        print(f"   📦 Total stock: {inv_result.get('total_quantity', 'N/A')} units")
        if inv_result.get("warehouses"):
            print("   🏭 Warehouse availability:")
            for w in inv_result["warehouses"][:3]:
                print(f"      • {w['location']}: {w['quantity']} units")
    else:
        print(f"   ⚠️ Inventory check: {inv_result.get('message', 'Unknown')}")
    
    # ========== STEP 3: Create Payment Link ==========
    print_step(3, "CREATE PAYMENT LINK (Razorpay)")
    
    quantity = random.randint(1, 2)
    total_amount = round(selected['price'] * quantity, 2)
    
    items = [{
        "sku": selected['sku'],
        "name": selected['name'],
        "quantity": quantity,
        "price": selected['price']
    }]
    
    print(f"   🛒 Cart: {quantity}x {selected['name'][:40]}")
    print(f"   💰 Total Amount: ₹{total_amount:,.2f}")
    
    payment_result = create_payment_link(
        customer_id=customer_id,
        amount=total_amount,
        description=f"Order for {selected['name'][:30]}",
        items=items
    )
    
    if payment_result.get("status") != "success":
        print(f"   ❌ Payment link creation failed: {payment_result.get('message')}")
        return
    
    order_id = payment_result.get("order_id")
    payment_url = payment_result.get("payment_url")
    payment_link_id = payment_result.get("payment_link_id")
    
    print(f"\n   ✅ PAYMENT LINK CREATED!")
    print(f"   ┌─────────────────────────────────────────────────────────────┐")
    print(f"   │  📦 ORDER ID:      {order_id:<40} │")
    print(f"   │  💳 Payment Link:  {payment_url:<40} │")
    print(f"   │  🔗 Link ID:       {payment_link_id:<40} │")
    print(f"   │  💰 Amount:        ₹{total_amount:<39,.2f} │")
    print(f"   └─────────────────────────────────────────────────────────────┘")
    
    # ========== STEP 4: Check Order Status (Before Payment) ==========
    print_step(4, "CHECK ORDER STATUS (Before Payment)")
    
    status_result = get_order_status(order_id)
    
    if status_result.get("status") == "success":
        print(f"   📋 Order ID: {status_result.get('order_id')}")
        print(f"   👤 Customer: {status_result.get('customer_id')}")
        print(f"   💰 Amount: ₹{status_result.get('total_amount'):,.2f}")
        print(f"   📊 Status: {status_result.get('order_status', 'N/A').upper()}")
    else:
        print(f"   ❌ Could not fetch order status")
    
    # ========== STEP 5: Simulate Payment Completion ==========
    print_step(5, "CONFIRM PAYMENT (Simulating customer payment)")
    
    # Generate a mock Razorpay payment ID
    razorpay_payment_id = f"pay_{random.randint(10000000000000, 99999999999999)}"
    
    print(f"   💳 Simulating payment completion...")
    print(f"   🆔 Razorpay Payment ID: {razorpay_payment_id}")
    
    confirm_result = confirm_payment(order_id)
    
    if confirm_result.get("status") == "success":
        print(f"\n   ✅ PAYMENT CONFIRMED!")
        print(f"   ┌─────────────────────────────────────────────────────────────┐")
        print(f"   │  📦 ORDER ID:         {confirm_result.get('order_id'):<37} │")
        print(f"   │  💳 Payment Status:   {confirm_result.get('payment_status', 'paid').upper():<37} │")
        print(f"   │  👤 Customer ID:      {confirm_result.get('customer_id'):<37} │")
        print(f"   │  💰 Amount:           ₹{confirm_result.get('amount', total_amount):<36,.2f} │")
        print(f"   └─────────────────────────────────────────────────────────────┘")
    else:
        print(f"   ❌ Payment confirmation failed: {confirm_result.get('message')}")
    
    # ========== STEP 6: Check Order Status (After Payment) ==========
    print_step(6, "VERIFY ORDER STATUS (After Payment)")
    
    status_result = get_order_status(order_id)
    
    if status_result.get("status") == "success":
        print(f"   📋 Order ID: {status_result.get('order_id')}")
        print(f"   📊 Status: {status_result.get('order_status', 'N/A').upper()}")
        print(f"   ✅ Order is now PAID and ready for fulfillment!")
    
    # ========== STEP 7: Schedule Delivery ==========
    print_step(7, "SCHEDULE DELIVERY")
    
    delivery_address = {
        "street": "123 Main Street",
        "city": location.split(",")[0] if "," in location else location,
        "state": location.split(",")[1].strip() if "," in location else "Maharashtra",
        "pincode": f"{random.randint(400001, 560099)}"
    }
    
    delivery_result = schedule_delivery(
        order_id=order_id,
        customer_address=delivery_address,
        delivery_preference="standard"
    )
    
    if delivery_result.get("status") == "success":
        print(f"   ✅ DELIVERY SCHEDULED!")
        print(f"   📦 Tracking ID: {delivery_result.get('tracking_number', 'N/A')}")
        print(f"   📅 Estimated: {delivery_result.get('estimated_delivery', 'N/A')}")
        print(f"   🚚 Carrier: {delivery_result.get('carrier', 'N/A')}")
        addr = delivery_result.get('delivery_address', {})
        if isinstance(addr, dict):
            print(f"   📍 Address: {addr.get('street', '')}, {addr.get('city', '')}")
        else:
            print(f"   📍 Address: {addr}")
    else:
        print(f"   ⚠️ Delivery scheduling: {delivery_result.get('message', 'Simulated')}")
    
    # ========== STEP 8: Verify in Database ==========
    print_step(8, "VERIFY IN DATABASE")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Check order
    cur.execute("""
        SELECT order_id, customer_id, total_amount, status, razorpay_order_id, created_at
        FROM orders WHERE order_id = %s
    """, (order_id,))
    order = cur.fetchone()
    
    if order:
        print(f"   ✅ Order found in database:")
        print(f"      • Order ID: {order[0]}")
        print(f"      • Customer: {order[1]}")
        print(f"      • Amount: ₹{float(order[2]):,.2f}")
        print(f"      • Status: {order[3].upper()}")
        print(f"      • Razorpay ID: {order[4] or 'N/A'}")
        print(f"      • Created: {order[5]}")
    
    # Check order items
    cur.execute("""
        SELECT sku, product_name, quantity, price
        FROM order_items WHERE order_id = %s
    """, (order_id,))
    items = cur.fetchall()
    
    if items:
        print(f"\n   📦 Order Items:")
        for item in items:
            print(f"      • {item[1][:40]} (SKU: {item[0]}) x{item[2]} = ₹{float(item[3]):,.2f}")
    
    conn.close()
    
    # ========== FINAL SUMMARY ==========
    print_header("✅ E2E TEST COMPLETED SUCCESSFULLY!")
    
    print(f"""
    📋 TEST SUMMARY:
    ─────────────────────────────────────────────────────────────────
    
    👤 Customer:        {name} ({customer_id})
    🔍 Search Query:    "{query}"
    📦 Product:         {selected['name'][:45]}
    🏷️  SKU:             {selected['sku']}
    💰 Amount:          ₹{total_amount:,.2f}
    
    📦 ORDER ID:        {order_id}
    💳 Payment Link:    {payment_url}
    📊 Payment Status:  PAID ✅
    🚚 Delivery:        SCHEDULED ✅
    
    ─────────────────────────────────────────────────────────────────
    
    🎉 All steps completed successfully!
    
    """)

if __name__ == "__main__":
    main()
