"""
Multi-Agent Demo - Shows All 6 Agents Working Independently
This demo showcases each agent as a separate entity handling its specialized task
"""
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from config.config import GEMINI_API_KEY
from utils.database import initialize_database
from agents.worker_agents import (
    recommendation_agent,
    inventory_agent,
    payment_agent,
    fulfillment_agent,
    loyalty_agent,
    post_purchase_agent
)
from google.adk.runners import InMemoryRunner

def setup_environment():
    """Setup the environment and initialize database"""
    print("=" * 80)
    print("🤖 Multi-Agent Retail System - All Agents Working Independently")
    print("=" * 80)
    
    if not GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found!")
        print("\nPlease set your Gemini API key in the .env file")
        sys.exit(1)
    
    print(f"\n✅ Gemini API Key configured")
    
    print("\n📊 Initializing database...")
    initialize_database()
    
    print("\n✅ System ready - All 6 agents initialized!")
    print("=" * 80)

async def run_agent(agent, agent_name, task_description, user_message):
    """Run a specific agent with a task"""
    print(f"\n{'🔹' * 40}")
    print(f"🤖 {agent_name.upper()} IS NOW WORKING")
    print(f"📋 Task: {task_description}")
    print(f"{'🔹' * 40}")
    print(f"\n💬 User Request: {user_message}\n")
    
    runner = InMemoryRunner(agent=agent)
    print(f"⚙️  {agent_name} Response:")
    await runner.run_debug(user_message)
    print(f"\n✅ {agent_name} completed its task!")
    print(f"{'─' * 80}\n")
    await asyncio.sleep(1)

async def complete_shopping_flow():
    """Demonstrate all 6 agents working independently on a complete shopping journey"""
    
    print("\n" + "=" * 80)
    print("🛒 COMPLETE SHOPPING FLOW - ALL 6 AGENTS WORKING INDEPENDENTLY")
    print("=" * 80)
    print("\nScenario: Customer CUST1001 wants to buy headphones")
    print("\n" + "=" * 80)
    
    input("\n▶️  Press Enter to start the agent workflow...")
    
    # Agent 1: RECOMMENDATION AGENT
    await run_agent(
        agent=recommendation_agent,
        agent_name="RECOMMENDATION AGENT",
        task_description="Suggest suitable headphones for the customer",
        user_message="I'm looking for wireless headphones for daily use. Customer ID: CUST1001"
    )
    
    input("▶️  Press Enter to continue to next agent...")
    
    # Agent 2: INVENTORY AGENT
    await run_agent(
        agent=inventory_agent,
        agent_name="INVENTORY AGENT",
        task_description="Check stock availability at customer's location",
        user_message="Check if SKU1007 (Wireless Bluetooth Headphones) is available in New York - 5th Avenue store"
    )
    
    input("▶️  Press Enter to continue to next agent...")
    
    # Agent 3: LOYALTY AGENT
    await run_agent(
        agent=loyalty_agent,
        agent_name="LOYALTY & OFFERS AGENT",
        task_description="Check customer's loyalty tier and apply discounts",
        user_message="What's the loyalty status for customer CUST1001? Apply any available discounts for SKU1007"
    )
    
    input("▶️  Press Enter to continue to next agent...")
    
    # Agent 4: PAYMENT AGENT
    await run_agent(
        agent=payment_agent,
        agent_name="PAYMENT AGENT",
        task_description="Process payment for the purchase",
        user_message="Process payment for customer CUST1001. SKU: SKU1007, quantity: 1. Use saved Visa card ending in 4242"
    )
    
    input("▶️  Press Enter to continue to next agent...")
    
    # Agent 5: FULFILLMENT AGENT
    await run_agent(
        agent=fulfillment_agent,
        agent_name="FULFILLMENT AGENT",
        task_description="Arrange delivery for the purchased items",
        user_message="Schedule home delivery for customer CUST1001 to address: 123 Main St, New York, NY 10001. Order contains SKU1007"
    )
    
    input("▶️  Press Enter to continue to next agent...")
    
    # Agent 6: POST-PURCHASE AGENT
    await run_agent(
        agent=post_purchase_agent,
        agent_name="POST-PURCHASE SUPPORT AGENT",
        task_description="Handle post-purchase support and feedback",
        user_message="Customer CUST1001 wants to leave a review for their recent purchase of SKU1007. Rating: 5 stars. Comment: 'Great sound quality!'"
    )
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE WORKFLOW FINISHED - ALL 6 AGENTS WORKED INDEPENDENTLY!")
    print("=" * 80)

async def individual_agent_demo():
    """Let user interact with individual agents"""
    
    agents_menu = {
        "1": (recommendation_agent, "Recommendation Agent", "Get product recommendations"),
        "2": (inventory_agent, "Inventory Agent", "Check product availability"),
        "3": (loyalty_agent, "Loyalty & Offers Agent", "Check loyalty status and discounts"),
        "4": (payment_agent, "Payment Agent", "Process payments"),
        "5": (fulfillment_agent, "Fulfillment Agent", "Arrange delivery/pickup"),
        "6": (post_purchase_agent, "Post-Purchase Agent", "Handle returns and reviews")
    }
    
    while True:
        print("\n" + "=" * 80)
        print("🤖 SELECT AN AGENT TO INTERACT WITH")
        print("=" * 80)
        
        for key, (_, name, desc) in agents_menu.items():
            print(f"  {key}. {name} - {desc}")
        print("  0. Back to main menu")
        print("=" * 80)
        
        choice = input("\n👉 Select agent (0-6): ").strip()
        
        if choice == "0":
            break
        
        if choice not in agents_menu:
            print("\n❌ Invalid choice!")
            continue
        
        agent, agent_name, _ = agents_menu[choice]
        
        print(f"\n{'🔹' * 40}")
        print(f"🤖 Now interacting with: {agent_name.upper()}")
        print(f"{'🔹' * 40}")
        
        user_message = input(f"\n💬 Your message to {agent_name}: ").strip()
        
        if user_message:
            runner = InMemoryRunner(agent=agent)
            print(f"\n⚙️  {agent_name} Response:")
            await runner.run_debug(user_message)
            print()
        
        input("\n✅ Press Enter to continue...")

async def parallel_agents_demo():
    """Show multiple agents working in parallel on different tasks"""
    
    print("\n" + "=" * 80)
    print("⚡ PARALLEL AGENT EXECUTION - Multiple Agents Working Simultaneously")
    print("=" * 80)
    print("\nDemonstrating 3 customers being served by different agents at the same time")
    print("=" * 80)
    
    input("\n▶️  Press Enter to start parallel execution...")
    
    # Create tasks for different agents
    tasks = [
        run_agent(
            recommendation_agent,
            "RECOMMENDATION AGENT (Customer A)",
            "Finding products for Customer A",
            "Show me laptops for customer CUST1002"
        ),
        run_agent(
            inventory_agent,
            "INVENTORY AGENT (Customer B)",
            "Checking stock for Customer B",
            "Check stock for SKU3001 at all locations"
        ),
        run_agent(
            loyalty_agent,
            "LOYALTY AGENT (Customer C)",
            "Checking discounts for Customer C",
            "What loyalty tier is customer CUST1004? Show available offers"
        )
    ]
    
    # Run all tasks in parallel
    print("\n🚀 All 3 agents are now working simultaneously...\n")
    await asyncio.gather(*tasks)
    
    print("\n" + "=" * 80)
    print("✅ All parallel tasks completed!")
    print("=" * 80)

def print_main_menu():
    """Print main menu"""
    print("\n" + "=" * 80)
    print("🤖 MULTI-AGENT DEMO - MAIN MENU")
    print("=" * 80)
    print("\n  1. Complete Shopping Flow (All 6 Agents Sequential)")
    print("  2. Individual Agent Interaction")
    print("  3. Parallel Agent Execution Demo")
    print("  0. Exit")
    print("=" * 80)

async def main():
    """Main application"""
    setup_environment()
    
    while True:
        print_main_menu()
        choice = input("\n👉 Enter your choice (0-3): ").strip()
        
        if choice == "0":
            print("\n👋 Thank you for using the Multi-Agent System!")
            break
        elif choice == "1":
            await complete_shopping_flow()
        elif choice == "2":
            await individual_agent_demo()
        elif choice == "3":
            await parallel_agents_demo()
        else:
            print("\n❌ Invalid choice. Please select 0-3.")
        
        if choice in ["1", "2", "3"]:
            input("\n✅ Press Enter to return to main menu...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
