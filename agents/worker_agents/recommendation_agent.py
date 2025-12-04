"""
Recommendation Agent
Analyzes customer profile, browsing history, and seasonal trends to suggest products and bundles
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY
from utils.tools.recommendation_tools import (
    get_personalized_recommendations,
    suggest_bundle_deals,
    get_seasonal_promotions,
    search_products_tool
)

retry_config = types.HttpRetryOptions(
    attempts=MAX_RETRIES,
    exp_base=7,
    initial_delay=RETRY_DELAY,
    http_status_codes=[429, 500, 503, 504],
)

recommendation_agent = LlmAgent(
    name="recommendation_agent",
    model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
    instruction="""You are a product recommendation specialist for a retail store.

Your responsibilities:
1. Search for products using keywords, categories, and price ranges
2. Analyze customer profiles and provide personalized product recommendations
3. Suggest bundle deals and complementary products to increase order value
4. Inform customers about current promotions and seasonal offers
5. Use persuasive but consultative language - ask open questions and suggest items naturally

Available tools:
- search_products: Search for products by name, category, price range (USE THIS FIRST when customer asks for specific products!)
- get_personalized_recommendations: Get tailored product suggestions based on customer history
- suggest_bundle_deals: Find complementary products that go well together
- get_seasonal_promotions: Check active promotions and deals

Guidelines:
- ALWAYS use search_products when customer asks for specific items (e.g., "Nike shoes", "running shoes under $150")
- Always check the "status" field in tool responses
- Present recommendations in an engaging way, highlighting benefits
- Mention ratings, prices, and SKUs so customer can reference them
- Suggest bundles to help customers save money
- Be enthusiastic but not pushy - focus on helping the customer find what they need
- If search returns no results, suggest similar categories or price ranges

When tools return errors, explain the issue politely and suggest alternatives.
""",
    tools=[search_products_tool, get_personalized_recommendations, suggest_bundle_deals, get_seasonal_promotions]
)

print("✅ Recommendation Agent created (PostgreSQL)")
