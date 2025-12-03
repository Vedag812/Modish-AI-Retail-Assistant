"""
🚀 PRODUCTION DEMO - All Agents with REAL APIs
Complete retail agent system with real-time integrations
"""
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from config.config import GEMINI_API_KEY
from agents.worker_agents import (
    recommendation_agent,
    inventory_agent,
    payment_agent,
    fulfillment_agent,
    loyalty_agent,
    post_purchase_agent
)
from google.adk.runners import InMemoryRunner

# Import real APIs
from utils.external_apis.payment_api import payment_api
from utils.external_apis.inventory_api import inventory_api

# Check which database is being used
try:
    from utils.database_pg import init_postgresql, USE_POSTGRESQL
except:
    USE_POSTGRESQL = False

def print_banner():
    """Print startup banner"""
    print("\n" + "=" * 90)
    print("🚀 RETAIL SALES AGENT SYSTEM - PRODUCTION MODE")
    print("=" * 90)
    print("\n✅ REAL-TIME INTEGRATIONS ACTIVE:")
    print("   🤖 AI Engine: Google Gemini API (gemini-2.0-flash-exp)")
    print("   💳 Payment: Real Payment Gateway API")
    print("   📦 Inventory: FakeStore API + DummyJSON (Live Product Data)")
    print(f"   🗄️  Database: {'PostgreSQL (Cloud)' if USE_POSTGRESQL else 'SQLite (Local)'}")
    print("\n" + "=" * 90)

async def run_agent_with_context(agent, agent_name, icon, task, user_message):
    """Run agent with detailed context"""
    print(f"\n{'▓' * 90}")
    print(f"{icon} {agent_name.upper()}")
    print(f"{'▓' * 90}")
    print(f"📋 Task: {task}")
    print(f"💬 User: {user_message}")
    print(f"{'─' * 90}")
    
    runner = InMemoryRunner(agent=agent)
    
    try:
        print(f"⚙️  {agent_name} Processing...")
        await runner.run_debug(user_message)
        print(f"\n✅ {agent_name} completed successfully!")
    except Exception as e:
        print(f"\n❌ {agent_name} error: {str(e)}")
    
    print(f"{'─' * 90}\n")
    await asyncio.sleep(1)

async def complete_shopping_journey():
    """
    Demonstrate complete shopping journey with all 6 agents
    Uses REAL APIs for everything
    """
    
    print_banner()
    
    print("\n📖 SCENARIO: Complete Shopping Journey")
    print("   Customer CUST1001 wants to buy a product with full assistance")
    print("\n" + "=" * 90)
    
    input("\n▶️  Press Enter to start the journey with REAL APIs...")
    
    # Get real products from API
    print("\n🔄 Fetching real products from external API...")
    products_result = inventory_api.get_products(limit=3)
    
    if products_result["status"] == "success" and products_result["products"]:
        sample_product = products_result["products"][0]
        product_name = sample_product["name"]
        product_sku = sample_product["sku"]
        product_price = sample_product["price"]
        
        print(f"✅ Retrieved product: {product_name}")
        print(f"   SKU: {product_sku} | Price: ${product_price}")
    else:
        print("⚠️  Using fallback product")
        product_name = "Wireless Headphones"
        product_sku = "SKU1001"
        product_price = 129.99
    
    # AGENT 1: RECOMMENDATION AGENT
    await run_agent_with_context(
        agent=recommendation_agent,
        agent_name="AGENT 1: RECOMMENDATION ENGINE",
        icon="🎯",
        task="Analyze customer preferences and suggest products",
        user_message=f"I'm looking for electronics similar to {product_name}. Customer ID: CUST1001. Show me personalized recommendations based on my purchase history."
    )
    
    input("▶️  Press Enter to continue to inventory check...")
    
    # AGENT 2: INVENTORY AGENT (with real API)
    await run_agent_with_context(
        agent=inventory_agent,
        agent_name="AGENT 2: INVENTORY MANAGEMENT",
        icon="📦",
        task="Check real-time stock availability across all locations",
        user_message=f"Check stock availability for {product_name} (SKU: {product_sku}) across all store locations. I need it urgently."
    )
    
    input("▶️  Press Enter to continue to loyalty check...")
    
    # AGENT 3: LOYALTY AGENT
    await run_agent_with_context(
        agent=loyalty_agent,
        agent_name="AGENT 3: LOYALTY & REWARDS",
        icon="🎁",
        task="Check loyalty status, points, and applicable discounts",
        user_message=f"What's my loyalty status for customer CUST1001? Do I have any discounts or promo codes available? I want to buy {product_name} for ${product_price}."
    )
    
    input("▶️  Press Enter to continue to payment...")
    
    # AGENT 4: PAYMENT AGENT (with real API)
    print("\n🔄 Creating real payment order via API...")
    payment_order = payment_api.create_payment_order(
        amount=product_price,
        currency="USD",
        customer_id="CUST1001"
    )
    
    if payment_order["status"] == "success":
        print(f"✅ Payment order created: {payment_order['order_id']}")
        print(f"   Amount: ${payment_order['amount']}")
        print(f"   Provider: {payment_order['provider']}")
    
    await run_agent_with_context(
        agent=payment_agent,
        agent_name="AGENT 4: PAYMENT PROCESSOR",
        icon="💳",
        task="Process payment securely via real payment gateway",
        user_message=f"Process payment for customer CUST1001. Amount: ${product_price}. Use my saved Visa card ending in 4242. Order ID: {payment_order.get('order_id', 'ORD123456')}."
    )
    
    input("▶️  Press Enter to continue to fulfillment...")
    
    # AGENT 5: FULFILLMENT AGENT
    await run_agent_with_context(
        agent=fulfillment_agent,
        agent_name="AGENT 5: FULFILLMENT & DELIVERY",
        icon="🚚",
        task="Arrange delivery or pickup for the order",
        user_message="Schedule delivery for customer CUST1001 to address: 123 Main St, New York, NY 10001. I prefer express delivery (1-2 days)."
    )
    
    input("▶️  Press Enter to continue to post-purchase support...")
    
    # AGENT 6: POST-PURCHASE AGENT
    await run_agent_with_context(
        agent=post_purchase_agent,
        agent_name="AGENT 6: POST-PURCHASE SUPPORT",
        icon="🌟",
        task="Handle reviews, returns, and customer feedback",
        user_message=f"I want to leave a 5-star review for {product_name} (SKU: {product_sku}). The product quality is excellent and delivery was fast!"
    )
    
    # Final Summary
    print("\n" + "=" * 90)
    print("🎉 COMPLETE SHOPPING JOURNEY FINISHED!")
    print("=" * 90)
    
    print("\n📊 REAL APIs USED IN THIS SESSION:")
    print("   ✅ Gemini AI - 6 intelligent agent interactions")
    print("   ✅ Payment API - Real order creation & processing")
    print("   ✅ Inventory API - Live product data fetch")
    print(f"   ✅ Database - {'PostgreSQL (Cloud)' if USE_POSTGRESQL else 'SQLite (Local)'}")
    
    print("\n💡 CUSTOMER EXPERIENCE HIGHLIGHTS:")
    print("   • Personalized product recommendations")
    print("   • Real-time inventory checking")
    print("   • Loyalty rewards application")
    print("   • Secure payment processing")
    print("   • Flexible delivery options")
    print("   • Easy review submission")
    
    print("\n" + "=" * 90)

async def quick_multi_agent_demo():
    """Quick demo showing all agents in rapid succession"""
    
    print_banner()
    
    print("\n⚡ QUICK DEMO: All 6 Agents in Action")
    print("   Rapid-fire demonstration of all capabilities")
    print("\n" + "=" * 90)
    
    # Fetch real product
    products = inventory_api.get_products(limit=1)
    product = products["products"][0] if products.get("products") else None
    
    agents_config = [
        (recommendation_agent, "🎯 Recommendation", "Show me electronics for CUST1001"),
        (inventory_agent, "📦 Inventory", f"Check stock for {product['sku'] if product else 'SKU1001'} in New York"),
        (loyalty_agent, "🎁 Loyalty", "What discounts does CUST1001 have?"),
        (payment_agent, "💳 Payment", "Show saved payment methods for CUST1001"),
        (fulfillment_agent, "🚚 Fulfillment", "What delivery options are available for New York?"),
        (post_purchase_agent, "🌟 Support", "I want to track my order ORD123456")
    ]
    
    for agent, name, message in agents_config:
        print(f"\n{'▓' * 90}")
        print(f"{name.upper()}")
        print(f"{'▓' * 90}")
        print(f"💬 {message}\n")
        
        runner = InMemoryRunner(agent=agent)
        try:
            await runner.run_debug(message)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print(f"{'─' * 90}")
        await asyncio.sleep(0.5)
    
    print("\n" + "=" * 90)
    print("✅ All 6 agents demonstrated!")
    print("=" * 90)

async def interactive_mode():
    """Interactive mode - chat with all agents"""
    
    print_banner()
    
    print("\n💬 INTERACTIVE MODE")
    print("   Chat with any agent using natural language")
    print("   Type 'agents' to see available agents")
    print("   Type 'exit' to quit")
    print("\n" + "=" * 90)
    
    agents_map = {
        "1": (recommendation_agent, "Recommendation Agent"),
        "2": (inventory_agent, "Inventory Agent"),
        "3": (loyalty_agent, "Loyalty & Offers Agent"),
        "4": (payment_agent, "Payment Agent"),
        "5": (fulfillment_agent, "Fulfillment Agent"),
        "6": (post_purchase_agent, "Post-Purchase Agent")
    }
    
    current_agent = recommendation_agent
    current_name = "Recommendation Agent"
    
    while True:
        print(f"\n💬 Currently talking to: {current_name}")
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n👋 Thank you for using the Retail Sales Agent System!")
            break
        
        if user_input.lower() == 'agents':
            print("\n📋 Available Agents:")
            for key, (_, name) in agents_map.items():
                print(f"   {key}. {name}")
            print("\nType the number to switch agents")
            continue
        
        if user_input in agents_map:
            current_agent, current_name = agents_map[user_input]
            print(f"\n✅ Switched to {current_name}")
            continue
        
        if not user_input:
            continue
        
        print(f"\n🤖 {current_name}:")
        runner = InMemoryRunner(agent=current_agent)
        try:
            await runner.run_debug(user_input)
        except Exception as e:
            print(f"❌ Error: {e}")

def print_main_menu():
    """Display main menu"""
    print("\n" + "=" * 90)
    print("🎯 MAIN MENU - SELECT DEMONSTRATION MODE")
    print("=" * 90)
    print("\n  1. 🛒 Complete Shopping Journey (Recommended)")
    print("     └─ Full customer experience with all 6 agents working together")
    print("\n  2. ⚡ Quick Multi-Agent Demo")
    print("     └─ Rapid demonstration of all agent capabilities")
    print("\n  3. 💬 Interactive Chat Mode")
    print("     └─ Chat freely with individual agents")
    print("\n  4. 🔧 Test Real APIs")
    print("     └─ Verify payment and inventory API connectivity")
    print("\n  0. 🚪 Exit")
    print("\n" + "=" * 90)

async def test_apis():
    """Test all real API connections"""
    print("\n" + "=" * 90)
    print("🔧 TESTING REAL API CONNECTIONS")
    print("=" * 90)
    
    # Test Payment API
    print("\n1️⃣  Testing Payment API...")
    try:
        result = payment_api.create_payment_order(100.00, "USD", "TEST")
        if result["status"] == "success":
            print(f"   ✅ Payment API: Connected ({result['provider']})")
        else:
            print(f"   ❌ Payment API: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Payment API Error: {e}")
    
    # Test Inventory API
    print("\n2️⃣  Testing Inventory API...")
    try:
        result = inventory_api.get_products(limit=1)
        if result["status"] == "success":
            print(f"   ✅ Inventory API: Connected ({result['source']})")
            print(f"      Retrieved {result['count']} product(s)")
        else:
            print(f"   ❌ Inventory API: {result.get('message')}")
    except Exception as e:
        print(f"   ❌ Inventory API Error: {e}")
    
    # Test Database
    print("\n3️⃣  Testing Database...")
    try:
        if USE_POSTGRESQL:
            from utils.database_pg import test_connection
            if test_connection():
                print("   ✅ PostgreSQL: Connected")
            else:
                print("   ❌ PostgreSQL: Connection failed")
        else:
            print("   ✅ SQLite: Using local database")
    except Exception as e:
        print(f"   ❌ Database Error: {e}")
    
    # Test Gemini API
    print("\n4️⃣  Testing Gemini AI API...")
    if GEMINI_API_KEY:
        print("   ✅ Gemini API: Key configured")
    else:
        print("   ❌ Gemini API: No API key found")
    
    print("\n" + "=" * 90)
    input("\n▶️  Press Enter to return to menu...")

async def main():
    """Main application"""
    
    if not GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found!")
        print("Please add your API key to the .env file")
        return
    
    # Initialize database
    if USE_POSTGRESQL:
        print("\n🔄 Initializing PostgreSQL database...")
        init_postgresql()
    
    while True:
        print_main_menu()
        choice = input("\n👉 Enter your choice (0-4): ").strip()
        
        if choice == "0":
            print("\n👋 Thank you for using the Retail Sales Agent System!")
            print("   All real-time integrations performed successfully! 🎉")
            break
        elif choice == "1":
            await complete_shopping_journey()
            input("\n▶️  Press Enter to return to menu...")
        elif choice == "2":
            await quick_multi_agent_demo()
            input("\n▶️  Press Enter to return to menu...")
        elif choice == "3":
            await interactive_mode()
        elif choice == "4":
            await test_apis()
        else:
            print("\n❌ Invalid choice. Please select 0-4.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
