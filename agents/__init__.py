"""
Agents Package Initialization
"""
from .sales_agent import sales_agent
from .worker_agents import (
    recommendation_agent,
    inventory_agent,
    payment_agent,
    fulfillment_agent,
    loyalty_agent,
    post_purchase_agent
)

__all__ = [
    'sales_agent',
    'recommendation_agent',
    'inventory_agent',
    'payment_agent',
    'fulfillment_agent',
    'loyalty_agent',
    'post_purchase_agent'
]

print("✅ All agents package initialized")
