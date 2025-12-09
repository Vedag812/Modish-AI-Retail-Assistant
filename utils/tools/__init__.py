"""
Tools initialization - exports all tools for easy import
Firebase Firestore - All tools use Google Firebase
"""
from .recommendation_tools import (
    get_personalized_recommendations,
    suggest_bundle_deals,
    get_seasonal_promotions,
    search_products_tool
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
    create_payment_link,
    get_order_status
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
    apply_promotion,
    calculate_final_price,
    register_new_customer,
    add_loyalty_points
)

from .post_purchase_tools import (
    initiate_return,
    request_exchange,
    submit_review,
    get_order_history,
    track_return
)

__all__ = [
    # Recommendation tools
    'get_personalized_recommendations',
    'suggest_bundle_deals',
    'get_seasonal_promotions',
    'search_products_tool',
    
    # Inventory tools
    'check_inventory',
    'get_fulfillment_options',
    'reserve_inventory',
    
    # Payment tools
    'process_payment',
    'get_saved_payment_methods',
    'apply_gift_card',
    'create_payment_link',
    
    # Fulfillment tools
    'schedule_delivery',
    'schedule_store_pickup',
    'notify_store_staff',
    'track_shipment',
    'update_delivery_address',
    
    # Loyalty tools
    'get_loyalty_status',
    'apply_promotion',
    'calculate_final_price',
    'register_new_customer',
    'add_loyalty_points',
    
    # Post-purchase tools
    'initiate_return',
    'request_exchange',
    'submit_review',
    'get_order_history',
    'track_return',
]

print("✅ All tools initialized (Firebase)")
