"""
Tools initialization - exports all tools for easy import
"""
from .recommendation_tools import (
    get_personalized_recommendations,
    suggest_bundle_deals,
    get_seasonal_promotions
)

from .inventory_tools import (
    check_inventory,
    get_fulfillment_options,
    reserve_inventory
)

from .payment_tools import (
    process_payment,
    get_saved_payment_methods,
    apply_gift_card,
    handle_payment_retry,
    calculate_split_payment
)

from .fulfillment_tools import (
    schedule_delivery,
    schedule_store_pickup,
    notify_store_staff,
    track_shipment,
    update_delivery_address
)

from .loyalty_tools import (
    get_loyalty_status,
    apply_loyalty_discount,
    apply_promo_code,
    calculate_final_pricing,
    check_personalized_offers
)

from .post_purchase_tools import (
    initiate_return,
    process_exchange,
    track_return_status,
    submit_product_review,
    request_order_modification,
    get_order_history
)

__all__ = [
    # Recommendation tools
    'get_personalized_recommendations',
    'suggest_bundle_deals',
    'get_seasonal_promotions',
    
    # Inventory tools
    'check_inventory',
    'get_fulfillment_options',
    'reserve_inventory',
    
    # Payment tools
    'process_payment',
    'get_saved_payment_methods',
    'apply_gift_card',
    'handle_payment_retry',
    'calculate_split_payment',
    
    # Fulfillment tools
    'schedule_delivery',
    'schedule_store_pickup',
    'notify_store_staff',
    'track_shipment',
    'update_delivery_address',
    
    # Loyalty tools
    'get_loyalty_status',
    'apply_loyalty_discount',
    'apply_promo_code',
    'calculate_final_pricing',
    'check_personalized_offers',
    
    # Post-purchase tools
    'initiate_return',
    'process_exchange',
    'track_return_status',
    'submit_product_review',
    'request_order_modification',
    'get_order_history',
]

print("✅ All tools initialized and ready")
