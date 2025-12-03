"""
Main Application - Retail Sales Agent System
Demonstrates the complete conversational AI sales agent in action
"""
import os
import sys
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from config.config import GEMINI_API_KEY
from utils.database import initialize_database
from agents.sales_agent import sales_agent
from google.adk.runners import InMemoryRunner

def setup_environment():
    """Setup the environment and initialize database"""
    print("=" * 80)
    print("🛒 Retail Sales Agent System - Initialization")
    print("=" * 80)
    
    # Check for API key
    if not GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found!")
        print("\nPlease set your Gemini API key:")
        print("PowerShell: $env:GEMINI_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with: GEMINI_API_KEY=your-api-key-here")
        sys.exit(1)
    
    print(f"\n✅ Gemini API Key configured")
    
    # Initialize database
    print("\n📊 Initializing database...")
    initialize_database()
    
    print("\n✅ System ready!")
    print("=" * 80)

async def run_conversation(runner, customer_id: str, messages: list):
    """Run a conversation with the sales agent"""
    print(f"\n{'=' * 80}")
    print(f"💬 Conversation with Customer: {customer_id}")
    print(f"{'=' * 80}\n")
    
    for i, message in enumerate(messages, 1):
        print(f"👤 Customer: {message}")
        print(f"\n🤖 Sales Agent:")
        
        response = await runner.run_debug(message)
        
        print(f"\n{'-' * 80}\n")
        
        # Small delay between messages for readability
        await asyncio.sleep(0.5)

async def demo_scenario_1():
    """Demo Scenario 1: Product Discovery → Checkout"""
    runner = InMemoryRunner(agent=sales_agent)
    
    conversation = [
        "Hi! I'm looking for a good pair of wireless headphones",
        "What do you have in stock? I'm customer CUST1001",
        "The Wireless Bluetooth Headphones sound good. Can you check if it's available for delivery to New York?",
        "Great! Can you show me my loyalty status and any discounts I can get?",
        "Perfect! I'd like to purchase 1 unit. Can you show me my saved payment methods?",
        "Use my Visa card ending in 4242. Also, can you arrange standard delivery to 123 Main St, New York, NY 10001?",
        "Thanks! That's all for now."
    ]
    
    await run_conversation(runner, "CUST1001", conversation)

async def demo_scenario_2():
    """Demo Scenario 2: Bundle Purchase with Promotions"""
    runner = InMemoryRunner(agent=sales_agent)
    
    conversation = [
        "Hello! I need a laptop for work. I'm customer CUST1002",
        "Show me laptops you have",
        "The Laptop 15.6 inch looks good. What accessories would go well with it?",
        "I'll take the laptop and the wireless mouse. Do you have any active promotions?",
        "I have promo code SAVE20. Can you apply it?",
        "Great! Process the payment with my UPI and schedule it for click & collect at the Chicago store"
    ]
    
    await run_conversation(runner, "CUST1002", conversation)

async def demo_scenario_3():
    """Demo Scenario 3: Post-Purchase Support"""
    runner = InMemoryRunner(agent=sales_agent)
    
    conversation = [
        "Hi, I'm CUST1003. I need to return a product from my recent order ORD12345",
        "The item arrived damaged. I want to return SKU2001 - the Men's Casual Shirt",
        "Can you track my return request RET123456?",
        "Also, I'd like to leave a 5-star review for the great customer service!"
    ]
    
    await run_conversation(runner, "CUST1003", conversation)

async def demo_scenario_4():
    """Demo Scenario 4: Omnichannel Experience"""
    runner = InMemoryRunner(agent=sales_agent)
    
    conversation = [
        "Hi! I was browsing your mobile app earlier and added a 4K Smart TV to my wishlist. I'm customer CUST1004",
        "Can you check if the 4K Smart TV 55 inch is in stock? I'm interested in buying it",
        "What are my pickup options? I prefer to pick it up in-store if possible",
        "Perfect! I'll pick it up at the New York store. But first, do I have any personalized offers?",
        "Excellent! Let's complete the purchase. Use my Mastercard and I'll pick it up this evening"
    ]
    
    await run_conversation(runner, "CUST1004", conversation)

async def interactive_mode():
    """Interactive chat mode with the sales agent"""
    runner = InMemoryRunner(agent=sales_agent)
    
    print(f"\n{'=' * 80}")
    print("💬 Interactive Mode - Chat with the Sales Agent")
    print("=" * 80)
    print("\nType 'exit' or 'quit' to end the conversation\n")
    
    customer_id = input("👤 Enter your Customer ID (e.g., CUST1001): ").strip()
    if not customer_id:
        customer_id = "CUST1001"
    
    print(f"\n🤖 Sales Agent: Hello! Welcome to our store. How can I help you today?\n")
    
    while True:
        user_input = input(f"👤 {customer_id}: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n🤖 Sales Agent: Thank you for shopping with us! Have a great day!\n")
            break
        
        if not user_input:
            continue
        
        print(f"\n🤖 Sales Agent:")
        await runner.run_debug(user_input)
        print()

def print_menu():
    """Print the demo menu"""
    print("\n" + "=" * 80)
    print("🛒 Retail Sales Agent System - Demo Scenarios")
    print("=" * 80)
    print("\nSelect a demo scenario:")
    print("  1. Product Discovery → Complete Purchase")
    print("  2. Bundle Purchase with Promotions")
    print("  3. Post-Purchase Support (Returns & Reviews)")
    print("  4. Omnichannel Shopping Experience")
    print("  5. Interactive Chat Mode")
    print("  0. Exit")
    print("=" * 80)

async def main():
    """Main application entry point"""
    setup_environment()
    
    while True:
        print_menu()
        choice = input("\n👉 Enter your choice (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 Thank you for using Retail Sales Agent System!")
            break
        elif choice == "1":
            await demo_scenario_1()
        elif choice == "2":
            await demo_scenario_2()
        elif choice == "3":
            await demo_scenario_3()
        elif choice == "4":
            await demo_scenario_4()
        elif choice == "5":
            await interactive_mode()
        else:
            print("\n❌ Invalid choice. Please select 0-5.")
        
        if choice in ["1", "2", "3", "4", "5"]:
            input("\n✅ Demo complete. Press Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
