"""
Configuration file for Retail Sales Agent System
Manages API keys and system settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("⚠️  Warning: GEMINI_API_KEY not found in environment variables.")
    print("Please set it using: $env:GEMINI_API_KEY='your-api-key-here' (PowerShell)")
    print("Or add it to a .env file")

# System Configuration
APP_NAME = "Retail_Sales_Agent_System"
USER_ID = "customer_user"

# Database Configuration - Firebase Firestore
FIREBASE_SERVICE_ACCOUNT_PATH = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
print("✅ Using Firebase Firestore")

# Model Configuration
DEFAULT_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.0-flash-exp"

# Agent Configuration
MAX_RETRIES = 5
RETRY_DELAY = 1

# Channel Types
CHANNELS = ["web_chat", "mobile_app", "whatsapp", "telegram", "in_store_kiosk", "voice_assistant"]

# Product Categories
PRODUCT_CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Sports & Outdoors",
    "Books",
    "Beauty & Personal Care",
    "Toys & Games",
    "Automotive"
]

# Loyalty Tiers
LOYALTY_TIERS = {
    "bronze": {"min_points": 0, "discount": 0.05},
    "silver": {"min_points": 500, "discount": 0.10},
    "gold": {"min_points": 1500, "discount": 0.15},
    "platinum": {"min_points": 3000, "discount": 0.20}
}

# Store Locations
STORE_LOCATIONS = [
    "New York - 5th Avenue",
    "Los Angeles - Beverly Hills",
    "Chicago - Michigan Ave",
    "Miami - Brickell",
    "Seattle - Downtown"
]

print("✅ Configuration loaded successfully")
