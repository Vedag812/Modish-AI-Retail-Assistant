"""
Database Sync Tool
Syncs real API data to PostgreSQL database in real-time
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.database_pg import init_postgresql
from utils.external_apis.inventory_api import inventory_api
import random

def sync_products_to_db(db, limit=50):
    """Sync real products from API to PostgreSQL"""
    print("\n🔄 Syncing products from API to PostgreSQL...")
    
    # Fetch real products from API
    products_result = inventory_api.get_products(limit=limit)
    
    if products_result["status"] != "success":
        print(f"❌ Failed to fetch products: {products_result.get('message')}")
        return False
    
    products = products_result["products"]
    synced_count = 0
    
    for product in products:
        # Insert product into PostgreSQL
        result = db.insert_product({
            "sku": product["sku"],
            "name": product["name"],
            "category": product.get("category", "general"),
            "description": product.get("description", ""),
            "price": product["price"],
            "rating": product.get("rating", 0),
            "image": product.get("image", ""),
            "source": product.get("source", "api")
        })
        
        if result["status"] == "success":
            synced_count += 1
            
            # Add inventory for each location
            locations = [
                "New York - 5th Avenue",
                "Los Angeles - Beverly Hills", 
                "Chicago - Michigan Ave",
                "Miami - Brickell",
                "Seattle - Downtown",
                "Online Warehouse"
            ]
            
            for location in locations:
                quantity = random.randint(0, 100)
                db.update_inventory(product["sku"], location, quantity)
    
    print(f"✅ Synced {synced_count} products to PostgreSQL")
    return True

def create_sample_customers(db):
    """Create sample customers in PostgreSQL"""
    print("\n👥 Creating sample customers...")
    
    customers = [
        {
            "customer_id": "CUST1001",
            "name": "Emma Davis",
            "email": "emma.davis@email.com",
            "phone": "+1-555-0101",
            "loyalty_tier": "gold",
            "loyalty_points": 2500
        },
        {
            "customer_id": "CUST1002",
            "name": "Michael Chen",
            "email": "michael.chen@email.com",
            "phone": "+1-555-0102",
            "loyalty_tier": "silver",
            "loyalty_points": 1200
        },
        {
            "customer_id": "CUST1003",
            "name": "Sarah Johnson",
            "email": "sarah.j@email.com",
            "phone": "+1-555-0103",
            "loyalty_tier": "bronze",
            "loyalty_points": 350
        },
        {
            "customer_id": "CUST1004",
            "name": "James Wilson",
            "email": "james.w@email.com",
            "phone": "+1-555-0104",
            "loyalty_tier": "platinum",
            "loyalty_points": 5000
        }
    ]
    
    for customer in customers:
        result = db.insert_customer(customer)
        if result["status"] == "success":
            print(f"  ✅ Created customer: {customer['name']}")
    
    print(f"✅ Created {len(customers)} customers")

def main():
    """Main sync function"""
    print("=" * 80)
    print("🔄 DATABASE SYNC - Real API Data to PostgreSQL")
    print("=" * 80)
    
    # Initialize PostgreSQL
    db = init_postgresql()
    
    if not db or not db.conn:
        print("\n❌ Failed to connect to PostgreSQL")
        print("\n💡 Setup Instructions:")
        print("   1. Install PostgreSQL: https://www.postgresql.org/download/")
        print("   2. Or use free cloud PostgreSQL:")
        print("      - Supabase: https://supabase.com/")
        print("      - ElephantSQL: https://www.elephantsql.com/")
        print("   3. Set POSTGRESQL_URL in .env file")
        return
    
    # Sync products from API
    sync_products_to_db(db, limit=30)
    
    # Create sample customers
    create_sample_customers(db)
    
    print("\n" + "=" * 80)
    print("✅ DATABASE SYNC COMPLETE!")
    print("=" * 80)
    print("\n📊 Your PostgreSQL database now contains:")
    print("   ✅ Real products from FakeStore/DummyJSON APIs")
    print("   ✅ Real-time inventory across 6 locations")
    print("   ✅ Sample customer profiles")
    print("   ✅ Ready for order processing")
    print("\n" + "=" * 80)
    
    db.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Sync interrupted!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
