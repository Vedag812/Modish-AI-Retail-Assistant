# Firebase Setup Guide for Retail Sales Agent

This guide will help you set up Google Firebase Firestore for the Retail Sales Agent system.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Enter a project name (e.g., `retail-sales-agent`)
4. Disable Google Analytics (optional) and click **Create Project**
5. Wait for the project to be created

## Step 2: Enable Firestore Database

1. In your Firebase project, click **"Build"** in the left sidebar
2. Click **"Firestore Database"**
3. Click **"Create database"**
4. Select **"Start in test mode"** (for development)
   - ⚠️ For production, configure proper security rules
5. Choose your preferred location (e.g., `asia-south1` for India)
6. Click **"Enable"**

## Step 3: Generate Service Account Key

1. Click the **gear icon** ⚙️ next to "Project Overview"
2. Select **"Project settings"**
3. Go to the **"Service accounts"** tab
4. Click **"Generate new private key"**
5. Click **"Generate key"** to download the JSON file
6. **Save this file** as `firebase-service-account.json` in your project root

## Step 4: Configure Environment Variables

1. Open your `.env` file (or create one from `.env.example`)
2. Add the following line:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

Or if you're deploying to cloud, you can use the JSON content directly:

```env
FIREBASE_SERVICE_ACCOUNT_JSON={"type": "service_account", "project_id": "...", ...}
```

## Step 5: Populate the Database

Run the population script to add products, customers, and inventory:

```bash
python data/populate_firebase.py
```

This will add:
- 📦 1,200+ Indian products across 12 categories
- 👥 32 sample customers
- 🏪 6,000+ inventory entries (1,200 products × 5 warehouses)
- 🎁 5 promotional codes

## Firestore Structure

After running the population script, your Firestore will have these collections:

```
firestore/
├── customers/           # Customer profiles
│   └── CUST2001         # Document ID = customer_id
│       ├── name
│       ├── email
│       ├── phone
│       ├── location
│       ├── loyalty_tier
│       └── loyalty_points
│
├── products/            # Product catalog
│   └── IND1001          # Document ID = SKU
│       ├── name
│       ├── category
│       ├── current_price
│       ├── rating
│       └── reviews_count
│
├── inventory/           # Stock levels
│   └── IND1001_Mumbai_Warehouse
│       ├── sku
│       ├── location
│       ├── quantity
│       └── last_updated
│
├── orders/              # Customer orders
│   └── ORD123456
│       ├── customer_id
│       ├── items[]
│       ├── total_amount
│       ├── status
│       └── created_at
│
├── transactions/        # Payment transactions
│   └── TXN123456789
│       ├── order_id
│       ├── customer_id
│       ├── amount
│       ├── payment_method
│       └── status
│
└── promotions/          # Promo codes
    └── DIWALI20
        ├── description
        ├── discount_percent
        └── min_purchase
```

## Troubleshooting

### Error: Firebase credentials not found

Make sure your `.env` file has the correct path:
```env
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

### Error: Permission denied

1. Go to Firebase Console > Firestore > Rules
2. For development, use:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```
⚠️ **Note:** This is for development only. Use proper security rules in production.

### Error: firebase_admin not installed

Run:
```bash
pip install firebase-admin
```

## Verification

To verify your setup is working:

```python
from utils.firebase_db import get_db, get_products_count, get_all_customers

db = get_db()
print(f"Products: {get_products_count()}")
print(f"Customers: {len(get_all_customers())}")
```

Expected output:
```
✅ Firebase initialized from service account file
✅ Firestore database connected
Products: 1200
Customers: 32
```

## Production Security Rules

For production, update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Products - read only for everyone
    match /products/{productId} {
      allow read: if true;
      allow write: if false;
    }
    
    // Inventory - read only for everyone
    match /inventory/{inventoryId} {
      allow read: if true;
      allow write: if false;
    }
    
    // Customers - authenticated only
    match /customers/{customerId} {
      allow read, write: if request.auth != null;
    }
    
    // Orders - authenticated only
    match /orders/{orderId} {
      allow read, write: if request.auth != null;
    }
    
    // Promotions - read only
    match /promotions/{promoId} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

## Need Help?

- [Firebase Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
