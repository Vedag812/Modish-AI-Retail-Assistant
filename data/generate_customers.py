"""
Synthetic Customer Profile Generator
Creates realistic customer profiles with demographics, purchase history, 
loyalty tier, and device preferences for ≥10 customers
"""
import random
from datetime import datetime, timedelta
import json

# Sample data for realistic profiles
FIRST_NAMES = [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", 
    "Isabella", "James", "Mia", "Lucas", "Charlotte", "Benjamin", "Amelia",
    "Jackson", "Harper", "Alexander", "Evelyn", "Michael", "Abigail"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Seattle",
    "Denver", "Boston", "Miami", "Atlanta", "Portland", "Las Vegas"
]

CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden", "Sports & Outdoors",
    "Beauty & Personal Care", "Books", "Toys & Games", "Automotive",
    "Jewelry", "Groceries"
]

DEVICES = ["Mobile", "Desktop", "Tablet", "Smart TV", "Voice Assistant"]

LOYALTY_TIERS = {
    "bronze": {"min_points": 0, "max_points": 499, "discount": 0.05},
    "silver": {"min_points": 500, "max_points": 1499, "discount": 0.10},
    "gold": {"min_points": 1500, "max_points": 2999, "discount": 0.15},
    "platinum": {"min_points": 3000, "max_points": 10000, "discount": 0.20}
}

def generate_customer_profile(customer_id):
    """Generate a single synthetic customer profile"""
    
    # Demographics
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    age = random.randint(18, 70)
    city = random.choice(CITIES)
    
    # Determine loyalty tier and points
    tier = random.choice(list(LOYALTY_TIERS.keys()))
    tier_data = LOYALTY_TIERS[tier]
    loyalty_points = random.randint(tier_data["min_points"], tier_data["max_points"])
    
    # Purchase history (3-15 purchases)
    num_purchases = random.randint(3, 15)
    purchase_history = []
    total_spent = 0
    
    for i in range(num_purchases):
        category = random.choice(CATEGORIES)
        amount = round(random.uniform(15.99, 499.99), 2)
        days_ago = random.randint(1, 365)
        purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        purchase_history.append({
            "date": purchase_date,
            "category": category,
            "amount": amount,
            "items": random.randint(1, 5)
        })
        total_spent += amount
    
    # Sort by date (newest first)
    purchase_history.sort(key=lambda x: x["date"], reverse=True)
    
    # Favorite categories (based on purchase history)
    category_counts = {}
    for purchase in purchase_history:
        cat = purchase["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    favorite_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    favorite_categories = [cat for cat, _ in favorite_categories]
    
    # Device preferences (weighted random)
    devices_used = random.sample(DEVICES, k=random.randint(2, 4))
    primary_device = devices_used[0]
    
    # Calculate average order value
    avg_order_value = round(total_spent / num_purchases, 2) if num_purchases > 0 else 0
    
    # Customer segment based on behavior
    if avg_order_value > 200 and num_purchases > 10:
        segment = "VIP"
    elif avg_order_value > 100:
        segment = "High Value"
    elif num_purchases > 8:
        segment = "Frequent Buyer"
    else:
        segment = "Regular"
    
    # Join date (between 6 months and 3 years ago)
    days_member = random.randint(180, 1095)
    join_date = (datetime.now() - timedelta(days=days_member)).strftime("%Y-%m-%d")
    
    return {
        "customer_id": customer_id,
        "demographics": {
            "name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}@email.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "age": age,
            "city": city,
            "state": "NY" if city == "New York" else "CA" if city in ["Los Angeles", "San Diego", "San Jose"] else "TX"
        },
        "loyalty": {
            "tier": tier,
            "points": loyalty_points,
            "discount_rate": tier_data["discount"],
            "join_date": join_date
        },
        "purchase_history": purchase_history,
        "behavior": {
            "total_purchases": num_purchases,
            "total_spent": round(total_spent, 2),
            "avg_order_value": avg_order_value,
            "favorite_categories": favorite_categories,
            "segment": segment
        },
        "device_preferences": {
            "primary_device": primary_device,
            "devices_used": devices_used,
            "prefers_mobile": primary_device in ["Mobile", "Tablet"]
        }
    }

def generate_customer_profiles(count=10):
    """Generate multiple customer profiles"""
    profiles = []
    for i in range(count):
        customer_id = f"CUST{1001 + i}"
        profile = generate_customer_profile(customer_id)
        profiles.append(profile)
    
    return profiles

def save_profiles_to_file(profiles, filename="data/customer_profiles.json"):
    """Save profiles to JSON file"""
    import os
    os.makedirs("data", exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(profiles, f, indent=2)
    
    print(f"✅ Saved {len(profiles)} customer profiles to {filename}")

def load_profiles_from_file(filename="data/customer_profiles.json"):
    """Load profiles from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  File {filename} not found. Generating new profiles...")
        profiles = generate_customer_profiles(10)
        save_profiles_to_file(profiles, filename)
        return profiles

def print_profile_summary(profile):
    """Print a formatted summary of a customer profile"""
    print(f"\n{'='*70}")
    print(f"👤 {profile['demographics']['name']} ({profile['customer_id']})")
    print(f"{'='*70}")
    print(f"📧 {profile['demographics']['email']}")
    print(f"📱 {profile['demographics']['phone']}")
    print(f"📍 {profile['demographics']['city']}, {profile['demographics']['state']}")
    print(f"🎂 Age: {profile['demographics']['age']}")
    print(f"\n🎁 Loyalty: {profile['loyalty']['tier'].upper()} ({profile['loyalty']['points']} points)")
    print(f"💰 Total Spent: ${profile['behavior']['total_spent']:,.2f}")
    print(f"📊 Purchases: {profile['behavior']['total_purchases']} | Avg: ${profile['behavior']['avg_order_value']:.2f}")
    print(f"⭐ Segment: {profile['behavior']['segment']}")
    print(f"📱 Primary Device: {profile['device_preferences']['primary_device']}")
    print(f"🛍️  Favorite Categories: {', '.join(profile['behavior']['favorite_categories'])}")
    print(f"{'='*70}")

if __name__ == "__main__":
    # Generate 10 customer profiles
    print("🎭 Generating Synthetic Customer Profiles...\n")
    profiles = generate_customer_profiles(15)
    
    # Save to file
    save_profiles_to_file(profiles)
    
    # Display summary
    print(f"\n📊 Generated {len(profiles)} customer profiles")
    print(f"\n{'='*70}")
    print("CUSTOMER DISTRIBUTION:")
    print(f"{'='*70}")
    
    # Tier distribution
    tiers = {}
    segments = {}
    for p in profiles:
        tier = p['loyalty']['tier']
        segment = p['behavior']['segment']
        tiers[tier] = tiers.get(tier, 0) + 1
        segments[segment] = segments.get(segment, 0) + 1
    
    print("\n🎁 Loyalty Tiers:")
    for tier, count in sorted(tiers.items()):
        print(f"   {tier.capitalize()}: {count} customers")
    
    print("\n⭐ Customer Segments:")
    for segment, count in sorted(segments.items()):
        print(f"   {segment}: {count} customers")
    
    # Show first 3 profiles in detail
    print(f"\n{'='*70}")
    print("SAMPLE PROFILES (First 3):")
    for profile in profiles[:3]:
        print_profile_summary(profile)
    
    print(f"\n✅ All profiles saved to data/customer_profiles.json")
    print(f"💡 Use load_profiles_from_file() to load them in your code")
