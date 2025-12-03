"""
Worker Agents Initialization
Exports all worker agents for the retail sales system
"""
from .recommendation_agent import recommendation_agent
from .inventory_agent import inventory_agent
from .payment_agent import payment_agent
from .fulfillment_agent import fulfillment_agent
from .loyalty_agent import loyalty_agent
from .post_purchase_agent import post_purchase_agent

__all__ = [
    'recommendation_agent',
    'inventory_agent',
    'payment_agent',
    'fulfillment_agent',
    'loyalty_agent',
    'post_purchase_agent'
]

print("✅ All worker agents initialized")
