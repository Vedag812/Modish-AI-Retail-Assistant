"""
Real API Integration Demo
Shows agents using REAL external APIs (100% FREE)
"""
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from config.config import GEMINI_API_KEY
from utils.external_apis.payment_api import payment_api
from utils.external_apis.inventory_api import inventory_api

print("=" * 80)
print("🌐 REAL API INTEGRATION DEMO")
print("=" * 80)
print("\n✅ Using 100% FREE Public APIs:")
print("   - Payment: Mock Payment Gateway (Free)")
print("   - Inventory: FakeStore API + DummyJSON (Free)")
print("   - AI: Google Gemini API (Your key)")
print("\n" + "=" * 80)

async def demo_payment_api():
    """Demonstrate real payment API"""
    print("\n\n🔹 PAYMENT API DEMONSTRATION")
    print("─" * 80)
    
    print("\n1️⃣  Creating Payment Order...")
    order = payment_api.create_payment_order(
        amount=129.99,
        currency="USD",
        customer_id="CUST1001"
    )
    
    print(f"\n   Status: {order['status']}")
    print(f"   Order ID: {order.get('order_id', 'N/A')}")
    print(f"   Amount: ${order.get('amount', 0):.2f}")
    print(f"   Provider: {order.get('provider', 'N/A')}")
    
    if order["status"] == "success":
        print(f"   Payment URL: {order.get('payment_url', 'N/A')}")
        
        print("\n2️⃣  Verifying Payment...")
        verification = payment_api.verify_payment(
            order_id=order["order_id"],
            payment_id=f"PAY_TEST_{order['order_id']}"
        )
        
        print(f"\n   Verified: {'✅ Yes' if verification.get('verified') else '❌ No'}")
        print(f"   Transaction ID: {verification.get('transaction_id', 'N/A')}")
    
    await asyncio.sleep(1)

async def demo_inventory_api():
    """Demonstrate real inventory API"""
    print("\n\n🔹 INVENTORY API DEMONSTRATION")
    print("─" * 80)
    
    print("\n1️⃣  Fetching Real Products from API...")
    products = inventory_api.get_products(limit=5)
    
    if products["status"] == "success":
        print(f"\n   ✅ Retrieved {products['count']} products from {products['source']}")
        print("\n   📦 Sample Products:")
        
        for i, product in enumerate(products["products"][:3], 1):
            print(f"\n   {i}. {product['name']}")
            print(f"      SKU: {product['sku']}")
            print(f"      Price: ${product['price']:.2f}")
            print(f"      Category: {product['category']}")
            print(f"      Rating: ⭐ {product['rating']}/5")
            print(f"      Stock: {product['stock']} units")
    
    await asyncio.sleep(1)
    
    print("\n2️⃣  Checking Stock by Location...")
    if products["status"] == "success" and products["products"]:
        sku = products["products"][0]["sku"]
        stock_info = inventory_api.check_stock(sku)
        
        if stock_info["status"] == "success":
            print(f"\n   Product: {sku}")
            print(f"   Total Stock: {stock_info['total_stock']} units")
            print("\n   📍 Location Breakdown:")
            for loc, qty in stock_info["locations"].items():
                status = "✅ In Stock" if qty > 0 else "❌ Out of Stock"
                print(f"      {loc}: {qty} units - {status}")
    
    await asyncio.sleep(1)
    
    print("\n3️⃣  Getting Product Categories...")
    categories = inventory_api.get_categories()
    
    if categories["status"] == "success":
        print(f"\n   Available Categories ({categories['count']}):")
        for cat in categories["categories"]:
            print(f"      • {cat}")
    
    await asyncio.sleep(1)
    
    print("\n4️⃣  Searching Products...")
    search_results = inventory_api.search_products("shirt", limit=3)
    
    if search_results["status"] == "success":
        print(f"\n   Search Query: '{search_results['query']}'")
        print(f"   Results Found: {search_results['count']}")
        
        for i, product in enumerate(search_results["products"], 1):
            print(f"\n   {i}. {product['name']}")
            print(f"      ${product['price']:.2f} - ⭐ {product['rating']}/5")

async def demo_agents_with_real_apis():
    """Run agents with real API integration"""
    print("\n\n🔹 AGENTS USING REAL APIs")
    print("─" * 80)
    
    from agents.worker_agents import inventory_agent, payment_agent
    from google.adk.runners import InMemoryRunner
    
    print("\n1️⃣  Inventory Agent - Checking Real Product Stock...")
    products = inventory_api.get_products(limit=1)
    if products["status"] == "success" and products["products"]:
        product = products["products"][0]
        
        runner = InMemoryRunner(agent=inventory_agent)
        await runner.run_debug(f"Check stock for {product['name']} (SKU: {product['sku']}) at all locations")
    
    await asyncio.sleep(2)
    
    print("\n\n2️⃣  Payment Agent - Processing Real Payment...")
    runner = InMemoryRunner(agent=payment_agent)
    await runner.run_debug("Process payment for customer CUST1001, amount $129.99, using credit card")

async def main():
    """Main demo function"""
    
    if not GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found!")
        return
    
    try:
        # Demo 1: Payment API
        await demo_payment_api()
        
        # Demo 2: Inventory API
        await demo_inventory_api()
        
        # Demo 3: Agents with APIs
        await demo_agents_with_real_apis()
        
        print("\n\n" + "=" * 80)
        print("🎉 REAL API DEMO COMPLETE!")
        print("=" * 80)
        print("\n📊 Summary:")
        print("   ✅ Payment API - Working with real mock gateway")
        print("   ✅ Inventory API - Fetching real products from public APIs")
        print("   ✅ AI Agents - Using real Gemini API")
        print("\n💡 To use Razorpay (real payment gateway):")
        print("   1. Sign up at https://razorpay.com/ (Free test account)")
        print("   2. Get API keys from dashboard")
        print("   3. Add to .env file:")
        print("      RAZORPAY_KEY_ID=your_key_id")
        print("      RAZORPAY_KEY_SECRET=your_key_secret")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted!")
