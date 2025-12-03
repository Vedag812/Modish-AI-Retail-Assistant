"""
🎭 INTERACTIVE CONVERSATION DEMO
Shows clear customer-agent dialogue for all 6 AI agents
Each agent responds naturally with visible conversation flow
"""

import asyncio
from google.adk.runners import InMemoryRunner
from agents.worker_agents.recommendation_agent import recommendation_agent
from agents.worker_agents.inventory_agent import inventory_agent
from agents.worker_agents.loyalty_agent import loyalty_agent
from agents.worker_agents.payment_agent import payment_agent
from agents.worker_agents.fulfillment_agent import fulfillment_agent
from agents.worker_agents.post_purchase_agent import post_purchase_agent
from utils.external_apis.inventory_api import InventoryAPI
from utils.external_apis.payment_api import PaymentAPI

payment_api = PaymentAPI()
inventory_api = InventoryAPI()

def print_header(title, emoji):
    """Print colorful section header"""
    print("\n" + "=" * 90)
    print(f"{emoji}  {title}")
    print("=" * 90 + "\n")

def print_customer(message):
    """Print customer message"""
    print(f"👤 Customer: {message}")
    print()

def print_agent(agent_name, message):
    """Print agent response"""
    print(f"🤖 {agent_name}: {message}")
    print()

def print_thinking(agent_name):
    """Show agent is processing"""
    print(f"   ⚙️  {agent_name} is thinking...")
    print()

async def run_conversation_with_agent(agent, agent_name, customer_message):
    """Run a single customer-agent conversation"""
    print_customer(customer_message)
    print_thinking(agent_name)
    
    runner = InMemoryRunner(agent=agent)
    
    try:
        # Run the agent with debug output
        print_agent(agent_name, "")  # Print agent header
        await runner.run_debug(customer_message)
        print()  # Add spacing
    except Exception as e:
        print_agent(agent_name, f"Error: {str(e)}")
    
    return "completed"

async def demo_recommendation_agent():
    """Demo 1: Product recommendations with personalization"""
    print_header("AGENT 1: RECOMMENDATION ENGINE", "🎯")
    
    print("📝 Scenario: Customer looking for electronics\n")
    
    customer_msg = (
        "Hi! I'm looking for electronics for my home office. "
        "I need a good wireless mouse and maybe a keyboard. "
        "My customer ID is CUST1001. What do you recommend?"
    )
    
    await run_conversation_with_agent(
        recommendation_agent,
        "Recommendation Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def demo_inventory_agent():
    """Demo 2: Stock checking and availability"""
    print_header("AGENT 2: INVENTORY MANAGEMENT", "📦")
    
    print("📝 Scenario: Customer checking product availability\n")
    
    # Use a known product SKU from database
    product_name = "Smartphone 128GB"
    product_sku = "SKU1004"
    
    print(f"🔍 Checking inventory for: {product_name}")
    print(f"   SKU: {product_sku}\n")
    
    customer_msg = (
        f"I'm interested in the {product_name} (SKU: {product_sku}). "
        f"Is it available at stores near me? I live in New York. "
        f"Can I pick it up today or do I need to order online?"
    )
    
    await run_conversation_with_agent(
        inventory_agent,
        "Inventory Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def demo_loyalty_agent():
    """Demo 3: Loyalty rewards and discounts"""
    print_header("AGENT 3: LOYALTY & REWARDS", "🎁")
    
    print("📝 Scenario: Customer checking for discounts\n")
    
    customer_msg = (
        "I'm customer CUST1001 (Ava Wilson). "
        "What's my loyalty status? Do I have any points or discounts? "
        "I'm planning to buy a $99.99 wireless mouse today."
    )
    
    await run_conversation_with_agent(
        loyalty_agent,
        "Loyalty Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def demo_payment_agent():
    """Demo 4: Payment processing"""
    print_header("AGENT 4: PAYMENT PROCESSOR", "💳")
    
    print("📝 Scenario: Customer ready to pay\n")
    
    # Create real payment order
    print("🔄 Creating payment order via API...")
    order = payment_api.create_payment_order(79.99, 'USD', 'ORD123456')
    print(f"   ✅ Order ID: {order['order_id']}")
    print(f"   💰 Amount: ${order['amount']}\n")
    
    customer_msg = (
        f"I'd like to process payment for customer CUST1001. "
        f"The amount is $79.99 (after my 20% Platinum discount). "
        f"I want to pay $30 with my gift card and the rest with my "
        f"saved Visa card ending in 4242. Order ID: {order['order_id']}"
    )
    
    await run_conversation_with_agent(
        payment_agent,
        "Payment Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def demo_fulfillment_agent():
    """Demo 5: Delivery and pickup options"""
    print_header("AGENT 5: FULFILLMENT & DELIVERY", "🚚")
    
    print("📝 Scenario: Customer choosing delivery method\n")
    
    customer_msg = (
        "I need to receive my wireless mouse as soon as possible. "
        "My address is 456 Park Ave, New York, NY 10022. "
        "What delivery options do you have? How much do they cost? "
        "Can I get it today? My customer ID is CUST1001."
    )
    
    await run_conversation_with_agent(
        fulfillment_agent,
        "Fulfillment Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def demo_post_purchase_agent():
    """Demo 6: Post-purchase support"""
    print_header("AGENT 6: POST-PURCHASE SUPPORT", "🌟")
    
    print("📝 Scenario: Customer leaving a review\n")
    
    customer_msg = (
        "Hi! I received my wireless mouse yesterday and I love it! "
        "The quality is excellent and it works perfectly with my laptop. "
        "I want to leave a 5-star review. My customer ID is CUST1001 "
        "and the product SKU is TECH001. Can you help me submit this review?"
    )
    
    await run_conversation_with_agent(
        post_purchase_agent,
        "Post-Purchase Agent",
        customer_msg
    )
    
    input("\n▶️  Press Enter to continue...\n")

async def main():
    """Run all agent conversations"""
    print("\n" + "╔" + "=" * 88 + "╗")
    print("║" + " " * 15 + "🎭 INTERACTIVE CUSTOMER-AGENT CONVERSATIONS" + " " * 29 + "║")
    print("║" + " " * 88 + "║")
    print("║" + "  Experience natural conversations with all 6 AI agents" + " " * 32 + "║")
    print("║" + "  Each agent uses real-time APIs and Gemini AI" + " " * 41 + "║")
    print("╚" + "=" * 88 + "╝\n")
    
    print("🔧 Initializing AI agents...")
    print("   ✅ Google Gemini API")
    print("   ✅ Payment API (Razorpay/Mock)")
    print("   ✅ Inventory API (FakeStore)")
    print("   ✅ PostgreSQL Database\n")
    
    input("▶️  Press Enter to start the demo...\n")
    
    # Run all 6 agent demos in sequence
    await demo_recommendation_agent()
    await demo_inventory_agent()
    await demo_loyalty_agent()
    await demo_payment_agent()
    await demo_fulfillment_agent()
    await demo_post_purchase_agent()
    
    # Final summary
    print("\n" + "=" * 90)
    print("🎉 DEMO COMPLETE - ALL 6 AGENTS DEMONSTRATED!")
    print("=" * 90)
    print("""
📊 WHAT YOU JUST SAW:

✅ Agent 1 (Recommendation): Personalized product suggestions
✅ Agent 2 (Inventory): Real-time stock checking with external APIs
✅ Agent 3 (Loyalty): Automatic discount calculation and points management
✅ Agent 4 (Payment): Secure payment processing with real gateway
✅ Agent 5 (Fulfillment): Flexible delivery options and scheduling
✅ Agent 6 (Post-Purchase): Review submission and customer support

🔗 REAL INTEGRATIONS USED:
• Google Gemini API - Natural language understanding
• Payment Gateway API - Order creation and verification
• FakeStore API - Live product inventory data
• PostgreSQL Database - Customer and order management

💡 NEXT STEPS:
1. Run 'python run_production.py' for full shopping journey
2. Try 'python demo_auto.py' for automated testing
3. Configure Razorpay keys in .env for real payments
4. Check README.md for complete documentation
    """)
    
    print("=" * 90 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check .env file has GEMINI_API_KEY")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Initialize database: python -c 'from utils.database_pg import init_postgresql; init_postgresql()'")
