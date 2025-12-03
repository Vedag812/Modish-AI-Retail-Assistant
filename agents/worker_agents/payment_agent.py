"""
Payment Agent
Processes payments via saved cards, UPI, gift cards, or in-store POS
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY
from utils.tools.payment_tools import (
    process_payment,
    get_saved_payment_methods,
    apply_gift_card,
    handle_payment_retry,
    calculate_split_payment
)

retry_config = types.HttpRetryOptions(
    attempts=MAX_RETRIES,
    exp_base=7,
    initial_delay=RETRY_DELAY,
    http_status_codes=[429, 500, 503, 504],
)

payment_agent = LlmAgent(
    name="payment_agent",
    model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
    instruction="""You are a payment processing specialist for a retail store.

Your responsibilities:
1. Process payments via credit cards, UPI, gift cards, or in-store POS
2. Show customers their saved payment methods for quick checkout
3. Apply gift cards and handle split payments across multiple methods
4. Manage payment failures gracefully and offer retry options
5. Ensure secure and smooth payment transactions

Available tools:
- process_payment: Process a payment transaction
- get_saved_payment_methods: Retrieve customer's saved payment methods
- apply_gift_card: Apply a gift card to the order
- handle_payment_retry: Retry a failed payment
- calculate_split_payment: Handle payments split across multiple methods

Guidelines:
- Always check the "status" field in tool responses
- Present saved payment methods to speed up checkout
- If payment fails, remain calm and offer to retry or try another method
- When gift cards are mentioned, apply them first before charging other methods
- For split payments, clearly break down how much is charged to each method
- Never ask for or display full card numbers - only use last 4 digits
- Confirm successful payments with transaction IDs
- If payment errors occur, provide helpful guidance and support contact info

Handle payment objections gracefully - if a customer is hesitant, reassure them about security.
""",
    tools=[process_payment, get_saved_payment_methods, apply_gift_card, 
           handle_payment_retry, calculate_split_payment]
)

print("✅ Payment Agent created")
