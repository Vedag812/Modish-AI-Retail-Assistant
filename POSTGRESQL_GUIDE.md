# 🗄️ PostgreSQL Database Integration Guide

## ✅ What's Integrated

Your retail sales system now supports **PostgreSQL** - a free, open-source, production-grade database!

### Why PostgreSQL?
- ✅ **100% Free** - Open source, no licensing costs
- ✅ **Production Ready** - Used by millions of apps worldwide
- ✅ **Cloud or Local** - Run locally or use free cloud hosting
- ✅ **Real-time** - Live data updates
- ✅ **Scalable** - Handles millions of records

---

## 🚀 Quick Start Options

### Option 1: Local PostgreSQL (Recommended for Development)

#### Step 1: Install PostgreSQL
**Windows:**
```powershell
# Download installer from:
https://www.postgresql.org/download/windows/

# Or use chocolatey:
choco install postgresql
```

#### Step 2: Create Database
```powershell
# Open pgAdmin or psql terminal
createdb retail_sales
```

#### Step 3: Update .env File
```env
POSTGRESQL_URL=postgresql://postgres:your_password@localhost:5432/retail_sales
```

#### Step 4: Install Python Package
```powershell
pip install psycopg2-binary
```

#### Step 5: Sync Database
```powershell
python sync_database.py
```

---

### Option 2: Free Cloud PostgreSQL (No Installation!)

#### 🌟 Supabase (Recommended - Best Free Tier)
- **Free Tier**: 500MB database, unlimited API requests
- **Setup Time**: 2 minutes

**Steps:**
1. Go to https://supabase.com/
2. Click "Start your project" (free)
3. Create new project
4. Copy connection string from Settings → Database
5. Add to `.env`:
   ```env
   POSTGRESQL_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
   ```
6. Run: `python sync_database.py`

#### 🐘 ElephantSQL
- **Free Tier**: 20MB database
- **Setup Time**: 1 minute

**Steps:**
1. Go to https://www.elephantsql.com/
2. Create free "Tiny Turtle" plan
3. Copy connection URL
4. Add to `.env`:
   ```env
   POSTGRESQL_URL=your_elephantsql_url
   ```

#### ⚡ Neon
- **Free Tier**: 3GB database
- **Setup Time**: 2 minutes

**Steps:**
1. Go to https://neon.tech/
2. Sign up for free
3. Create project
4. Copy connection string
5. Add to `.env`

---

## 📦 Installation

### Required Package
```powershell
pip install psycopg2-binary
```

### Optional (for better performance)
```powershell
# If psycopg2-binary doesn't work, try:
pip install psycopg2
```

---

## 🔧 Database Setup

### 1. Initialize Database
```powershell
python sync_database.py
```

This will:
- ✅ Create all tables (customers, products, inventory, orders, etc.)
- ✅ Sync real products from FakeStore/DummyJSON APIs
- ✅ Add inventory across 6 locations
- ✅ Create sample customer profiles

### 2. Verify Setup
The script will show:
```
✅ Connected to PostgreSQL database
✅ PostgreSQL tables created successfully
✅ Synced 30 products to PostgreSQL
✅ Created 4 customers
```

---

## 📊 Database Schema

### Tables Created:

1. **customers** - Customer profiles and loyalty data
   - customer_id, name, email, phone
   - loyalty_tier, loyalty_points
   - join_date

2. **products** - Product catalog
   - sku, name, category, description
   - current_price, rating, reviews_count
   - image_url, source

3. **inventory** - Stock management
   - sku, location, quantity
   - reserved, last_updated

4. **orders** - Order records
   - order_id, customer_id, status
   - total_amount, payment_method

5. **order_items** - Order line items
   - order_id, sku, quantity, price

6. **transactions** - Payment records
   - transaction_id, amount, status
   - provider, payment_method

7. **reviews** - Customer reviews
   - sku, customer_id, rating, comment

---

## 🎯 Using PostgreSQL with Agents

### Current Setup:
- ✅ PostgreSQL module ready (`utils/database_pg.py`)
- ✅ Sync script ready (`sync_database.py`)
- ✅ Real API data automatically synced

### Next Steps (Already Done):
The database can be queried for:
- Customer lookup
- Product search
- Inventory checking
- Order management
- Review storage

---

## 🔍 Testing Your Database

### Using pgAdmin (GUI):
1. Open pgAdmin
2. Connect to your database
3. View tables under `retail_sales` → Schemas → public → Tables

### Using psql (Command Line):
```powershell
# Connect to database
psql -U postgres -d retail_sales

# List tables
\dt

# View customers
SELECT * FROM customers;

# View products
SELECT * FROM products LIMIT 5;

# Check inventory
SELECT * FROM inventory WHERE location = 'New York - 5th Avenue';
```

### Using Python:
```python
from utils.database_pg import init_postgresql

# Connect
db = init_postgresql()

# Get customer
result = db.get_customer('CUST1001')
print(result)

# Search products
result = db.search_products('shirt')
print(result)

# Get inventory
result = db.get_inventory('API_1', 'New York - 5th Avenue')
print(result)
```

---

## 🔄 Data Flow

```
FakeStore/DummyJSON APIs
        ↓
    sync_database.py
        ↓
    PostgreSQL Database
        ↓
    Agent Tools
        ↓
    AI Agents (Gemini)
```

All data is REAL and stored in PostgreSQL!

---

## 💡 Benefits Over SQLite

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Concurrent Writes | ❌ No | ✅ Yes |
| Cloud Hosting | ❌ No | ✅ Yes |
| Advanced Features | ❌ Limited | ✅ Full SQL |
| Scalability | ❌ Limited | ✅ Unlimited |
| Real-time Sync | ❌ No | ✅ Yes |
| Production Ready | ⚠️ Small Apps | ✅ Enterprise |

---

## 🐛 Troubleshooting

### "Connection refused"
- **Local**: Make sure PostgreSQL is running
  ```powershell
  # Windows: Check services
  Get-Service -Name postgresql*
  ```
- **Cloud**: Check connection string is correct

### "Database does not exist"
```powershell
# Create database
createdb retail_sales

# Or using psql:
psql -U postgres
CREATE DATABASE retail_sales;
```

### "Password authentication failed"
- Check username/password in connection string
- Default PostgreSQL user is `postgres`
- Check `.env` file has correct credentials

### "psycopg2 not found"
```powershell
pip install psycopg2-binary
```

---

## 📈 Next Steps

1. **Run Sync**: `python sync_database.py`
2. **View Data**: Use pgAdmin or psql
3. **Test Agents**: Run demo with real PostgreSQL data
4. **Scale Up**: Add more products, customers, orders

---

## 🎁 Free Cloud PostgreSQL Comparison

| Provider | Free Storage | Connections | Best For |
|----------|-------------|-------------|----------|
| **Supabase** | 500MB | Unlimited | Best overall |
| **Neon** | 3GB | 100 | Most storage |
| **ElephantSQL** | 20MB | 5 | Quick start |

**Recommendation**: Start with **Supabase** for the best free tier!

---

## ✅ Summary

Your system now has:
- ✅ Real PostgreSQL database (local or cloud)
- ✅ Real products from APIs synced to PostgreSQL
- ✅ Real-time inventory management
- ✅ Production-ready database schema
- ✅ 100% free options available

**All your data is now stored in a REAL database!** 🎉
