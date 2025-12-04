"""
🛒 RETAIL SALES AGENT - Main Application
AI-Powered Multi-Agent Retail System with Orchestrated Workflow

Run this file to start the interactive shopping assistant.
All 6 AI agents work together automatically using Google Gemini API.
"""
import asyncio
import sys
import os
from google.adk.runners import InMemoryRunner
from google.genai import types
from agents.sales_agent.sales_agent import sales_agent

def init_database():
    """Initialize database with Indian dataset"""
    print("\n📊 Initializing database with Indian dataset...")
    try:
        # Add project root to path
        project_root = os.path.dirname(os.path.abspath(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Import and run the Indian dataset population
        from data.populate_india_dataset import main as populate_indian_data
        populate_indian_data()
        return True
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        import traceback
        traceback.print_exc()
        print("   Continuing with existing database...\n")
        return False

def print_banner():
    """Display application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║              🛒 RETAIL SALES AGENT v1.0                         ║
    ║                                                                  ║
    ║         AI-Powered Shopping Assistant with 6 Agents             ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    ✨ ALL 6 AI AGENTS WORKING TOGETHER:
    
       🎯 Recommendation Agent  - Personalized product suggestions
       📦 Inventory Agent       - Real-time stock checking
       🎁 Loyalty Agent         - Discounts & rewards
       💳 Payment Agent         - Razorpay integration
       🚚 Fulfillment Agent     - Delivery scheduling
       🌟 Support Agent         - Returns & reviews
    
    💬 JUST CHAT NATURALLY - Agents coordinate automatically!
    
    ══════════════════════════════════════════════════════════════════
    """
    print(banner)

def print_features():
    """Display feature list"""
    print("\n    🔗 ACTIVE INTEGRATIONS:")
    print("       ✓ Google Gemini AI (gemini-2.0-flash-exp)")
    print("       ✓ Razorpay Payment Gateway (Real API)")
    print("       ✓ PostgreSQL Database (Neon Cloud)")
    print("       ✓ FakeStore API (Product Catalog)")
    print("       ✓ DummyJSON API (Inventory)")
    print("\n    ══════════════════════════════════════════════════════════════════\n")

async def chat():
    """Main chat interface with orchestrated multi-agent system"""
    print_banner()
    print_features()
    
    runner = InMemoryRunner(agent=sales_agent)
    session_id = "retail_chat_session"
    user_id = "customer_user"
    
    # Create session before starting chat
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    print("    👋 Hi! I'm your AI Shopping Assistant.")
    print("    💡 Try: 'I want running shoes under ₹5000' or 'Check my rewards'\n")
    print("    Type 'quit' or 'exit' to end the session.\n")
    print("    " + "─" * 66 + "\n")
    
    while True:
        try:
            message = input("    👤 You: ").strip()
            
            if not message:
                continue
                
            if message.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n    " + "─" * 66)
                print("    👋 Thank you for shopping with us! Have a great day!")
                print("    " + "─" * 66 + "\n")
                break
            
            print(f"\n    🤖 AI Assistant:")
            print("    " + "─" * 66)
            
            # Initialize response tracking variables
            response_text = ""
            current_agent_display = None
            last_tool_agent = None
            agent_labels = {
                'sales_agent': '🛍️  Sales Agent',
                'recommendation_agent': '🎯 Recommendation Agent',
                'inventory_agent': '📦 Inventory Agent',
                'payment_agent': '💳 Payment Agent',
                'fulfillment_agent': '🚚 Fulfillment Agent',
                'loyalty_agent': '🎁 Loyalty Agent',
                'post_purchase_agent': '🌟 Support Agent'
            }
            
            # Map tool names to agent names
            tool_to_agent = {
                'recommendation_agent': 'recommendation_agent',
                'inventory_agent': 'inventory_agent',
                'payment_agent': 'payment_agent',
                'fulfillment_agent': 'fulfillment_agent',
                'loyalty_agent': 'loyalty_agent',
                'post_purchase_agent': 'post_purchase_agent',
                # Also map tool function patterns
                'search_products': 'recommendation_agent',
                'get_personalized_recommendations': 'recommendation_agent',
                'get_bundle_deals': 'recommendation_agent',
                'check_inventory': 'inventory_agent',
                'get_fulfillment_options': 'inventory_agent',
                'process_payment': 'payment_agent',
                'get_saved_payment_methods': 'payment_agent',
                'apply_gift_card': 'payment_agent',
                'schedule_delivery': 'fulfillment_agent',
                'schedule_store_pickup': 'fulfillment_agent',
                'get_loyalty_status': 'loyalty_agent',
                'apply_promotion': 'loyalty_agent',
                'calculate_final_price': 'loyalty_agent',
                'initiate_return': 'post_purchase_agent',
                'submit_review': 'post_purchase_agent',
                'get_order_history': 'post_purchase_agent',
            }

            def extract_text_from_event(event):
                """Extract text from ADK Event object."""
                text = ""
                
                # Check if event has content attribute (standard ADK Event)
                if hasattr(event, 'content') and event.content:
                    content = event.content
                    # Content might have parts
                    if hasattr(content, 'parts') and content.parts:
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                text += str(part.text)
                    # Or content might be a string directly
                    elif isinstance(content, str):
                        text += content
                    # Or content might have text attribute
                    elif hasattr(content, 'text') and content.text:
                        text += str(content.text)
                
                # Check for direct text attribute
                elif hasattr(event, 'text') and event.text:
                    text += str(event.text)
                
                # Check for parts directly on event
                elif hasattr(event, 'parts') and event.parts:
                    for part in event.parts:
                        if hasattr(part, 'text') and part.text:
                            text += str(part.text)
                
                return text
            
            # Stream response and track active agent
            # Convert string message to Content object with role
            content = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
            
            async for event in runner.run_async(
                new_message=content, 
                session_id=session_id, 
                user_id=user_id
            ):
                # Detect function/tool calls to identify worker agents
                detected_agent = None
                if hasattr(event, 'content') and event.content:
                    content_obj = event.content
                    if hasattr(content_obj, 'parts') and content_obj.parts:
                        for part in content_obj.parts:
                            # Check for function_call
                            if hasattr(part, 'function_call') and part.function_call:
                                func_name = part.function_call.name if hasattr(part.function_call, 'name') else str(part.function_call)
                                if func_name in tool_to_agent:
                                    detected_agent = tool_to_agent[func_name]
                                    last_tool_agent = detected_agent
                            # Check for function_response
                            elif hasattr(part, 'function_response') and part.function_response:
                                # Function response means a tool completed
                                if last_tool_agent:
                                    detected_agent = last_tool_agent
                
                # Determine which agent produced this event
                agent_name = None
                if detected_agent:
                    agent_name = detected_agent
                elif hasattr(event, 'author') and event.author:
                    agent_name = event.author
                elif hasattr(event, 'agent') and event.agent:
                    agent_name = event.agent.name if hasattr(event.agent, 'name') else str(event.agent)
                
                # Display agent label when it changes
                if agent_name:
                    display_name = agent_labels.get(agent_name, f'🤖 {agent_name}')
                    if display_name != current_agent_display:
                        if response_text:
                            print(f"    {response_text}\n")
                            response_text = ""
                        print(f"    [{display_name}]")
                        current_agent_display = display_name
                
                # Extract text from event
                extracted = extract_text_from_event(event)
                if extracted:
                    response_text += extracted
            
            # Display final response
            if response_text:
                print(f"    {response_text}")
            elif not current_agent_display:
                print("    [Response received]")
            
            print("    " + "─" * 66 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n    " + "─" * 66)
            print("    ⏸️  Shopping session interrupted.")
            print("    👋 See you next time!")
            print("    " + "─" * 66 + "\n")
            break
        except Exception as e:
            print(f"\n    ❌ Error: {e}")
            print("    💡 Please try again or type 'quit' to exit.\n")

async def main():
    """Application entry point"""
    try:
        await chat()
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check .env file has GEMINI_API_KEY")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Check your internet connection\n")
        sys.exit(1)

if __name__ == "__main__":
    print("\n🚀 Starting Retail Sales Agent...\n")
    
    skip_db_init = os.environ.get("SKIP_DB_INIT", "false").lower() in {"1", "true", "yes"}
    if skip_db_init:
        print("⚠️  SKIP_DB_INIT detected - skipping automatic database sync")
    else:
        init_database()
    
    # Start the chat application
    asyncio.run(main())