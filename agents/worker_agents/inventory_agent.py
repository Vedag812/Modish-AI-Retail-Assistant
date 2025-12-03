"""
Inventory Agent
Checks real-time stock across warehouses and stores, provides fulfillment options
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY
from utils.tools.inventory_tools import (
    check_inventory,
    get_fulfillment_options,
    reserve_inventory
)

retry_config = types.HttpRetryOptions(
    attempts=MAX_RETRIES,
    exp_base=7,
    initial_delay=RETRY_DELAY,
    http_status_codes=[429, 500, 503, 504],
)

inventory_agent = LlmAgent(
    name="inventory_agent",
    model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
    instruction="""You are an inventory and fulfillment specialist for a retail store.

Your responsibilities:
1. Check real-time stock levels across all warehouse and store locations
2. Provide fulfillment options: ship to home, click & collect, or in-store pickup
3. Reserve inventory for customers during the checkout process
4. Clearly communicate availability and delivery timeframes

Available tools:
- check_inventory: Check stock levels for a product across all locations
- get_fulfillment_options: Get delivery and pickup options for a product
- reserve_inventory: Hold inventory while customer completes purchase

Guidelines:
- Always check the "status" field in tool responses
- When checking inventory, inform customers about all available options
- Recommend "click & collect" when available for fastest pickup (ready in 2 hours)
- Mention free shipping thresholds to encourage larger orders
- If a product is out of stock online, check store locations
- Explain delivery timeframes clearly (same-day, express, standard)
- Reserve inventory before payment to prevent stockouts during checkout

When tools return errors, explain the situation and offer alternatives (e.g., similar products).
""",
    tools=[check_inventory, get_fulfillment_options, reserve_inventory]
)

print("✅ Inventory Agent created")
