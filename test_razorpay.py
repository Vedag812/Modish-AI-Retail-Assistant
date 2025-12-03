"""Test if Razorpay API is being used"""
from utils.external_apis.payment_api import payment_api

print("\n" + "=" * 60)
print("RAZORPAY CONNECTION TEST")
print("=" * 60)

print(f"\n🔍 Using Real API: {payment_api.use_real_api}")
print(f"🔑 Razorpay Key ID: {payment_api.razorpay_key_id}")
print(f"🔐 Has Secret: {'Yes' if payment_api.razorpay_key_secret else 'No'}")

print("\n📦 Creating test payment order...")
order = payment_api.create_payment_order(100.00, 'INR', 'TEST_CUSTOMER')

print(f"\n✅ Order Created:")
print(f"   Provider: {order.get('provider')}")
print(f"   Order ID: {order.get('order_id')}")
print(f"   Amount: {order.get('amount')} {order.get('currency', 'INR')}")
print(f"   Status: {order.get('status')}")

if order.get('provider') == 'razorpay':
    print("\n🎉 SUCCESS - Razorpay is ACTIVE!")
else:
    print("\n⚠️  Using Mock Gateway - Razorpay NOT active")

print("\n" + "=" * 60)
