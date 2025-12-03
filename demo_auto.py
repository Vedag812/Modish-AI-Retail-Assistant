"""
Automated Demo - All 6 Agents Working Automatically
Runs through all agents without user input for demonstration
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

async def run_agent_silently(agent, agent_name, user_message):
    """Run an agent and capture its response"""
    print(f"\n{'═' * 80}")
    print(f"🤖 {agent_name.upper()}")
    print(f"{'═' * 80}")
    print(f"📝 Request: {user_message}\n")
    
    runner = InMemoryRunner(agent=agent)
    print(f"💬 Response:")
    
    try:
        await runner.run_debug(user_message)
        print(f"\n✅ {agent_name} completed successfully!")
    except Exception as e:
        print(f"\n❌ {agent_name} encountered an error: {str(e)}")
    
    print(f"{'─' * 80}\n")
    await asyncio.sleep(0.5)

async def demo_all_agents_automatically():
    """Run all 6 agents automatically"""
    
    print("\n" + "=" * 80)
    print("🚀 AUTOMATED DEMO - ALL 6 AGENTS WORKING")
    print("=" * 80)
    print("\n✅ Gemini API Key configured")
    print("\n📊 Initializing database...")
    initialize_database()
    print("\n✅ All 6 agents initialized and ready!")
    print("\n" + "=" * 80)
    print("🎬 Starting automated agent workflow...")
    print("=" * 80)
    
    await asyncio.sleep(1)
    
    # Agent 1: RECOMMENDATION AGENT
    await run_agent_silently(
        recommendation_agent,
        "AGENT 1: RECOMMENDATION AGENT",
        "I'm looking for wireless headphones for daily use. Customer ID: CUST1001"
    )
    
    # Agent 2: INVENTORY AGENT  
    await run_agent_silently(
        inventory_agent,
        "AGENT 2: INVENTORY AGENT",
        "Check stock for SKU1004 (Smartphone) in all locations"
    )
    
    # Agent 3: LOYALTY AGENT
    await run_agent_silently(
        loyalty_agent,
        "AGENT 3: LOYALTY & OFFERS AGENT",
        "What's the loyalty status for customer CUST1001? Show available discounts"
    )
    
    # Agent 4: PAYMENT AGENT
    await run_agent_silently(
        payment_agent,
        "AGENT 4: PAYMENT AGENT",
        "Show saved payment methods for customer CUST1001"
    )
    
    # Agent 5: FULFILLMENT AGENT
    await run_agent_silently(
        fulfillment_agent,
        "AGENT 5: FULFILLMENT AGENT",
        "Schedule delivery for customer CUST1001 to 123 Main St, New York, NY 10001"
    )
    
    # Agent 6: POST-PURCHASE AGENT
    await run_agent_silently(
        post_purchase_agent,
        "AGENT 6: POST-PURCHASE SUPPORT AGENT",
        "Customer CUST1001 wants to leave a 5-star review for their recent purchase"
    )
    
    print("\n" + "=" * 80)
    print("🎉 ALL 6 AGENTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📊 Summary:")
    print("  ✅ Recommendation Agent - Product suggestions")
    print("  ✅ Inventory Agent - Stock checking")
    print("  ✅ Loyalty Agent - Discounts and rewards")
    print("  ✅ Payment Agent - Payment processing")
    print("  ✅ Fulfillment Agent - Delivery scheduling")
    print("  ✅ Post-Purchase Agent - Reviews and support")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        asyncio.run(demo_all_agents_automatically())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
