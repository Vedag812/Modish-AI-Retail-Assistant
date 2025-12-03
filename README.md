# 🛒 Retail Sales Agent System - Complete Guide

> **AI-Powered Multi-Agent Retail System with Real-Time Integrations**
> 
> A production-ready intelligent retail platform using Google Gemini AI, PostgreSQL, Razorpay Payments, and Live Inventory APIs

---

## 📑 Table of Contents
1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)
3. [Real-Time Integrations](#real-time-integrations)
4. [Installation & Setup](#installation--setup)
5. [Running the System](#running-the-system)
6. [Agent Capabilities](#agent-capabilities)
7. [API Configuration](#api-configuration)
8. [Database Setup](#database-setup)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (Currently using Python 3.13.7)
- PostgreSQL database (or use free Neon cloud database)
- Google Gemini API key (free tier available)
- Razorpay account (optional - mock mode available)

### Installation (5 minutes)

```powershell
# 1. Clone or navigate to project directory
cd c:\Users\VEDANT\retail_sales_agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Create .env file with these values:
```

**`.env` File Contents:**
```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# PostgreSQL Database URL (Required for production)
DATABASE_URL=postgresql://username:password@host:5432/database

# Razorpay Payment Gateway (Optional - uses mock if not set)
# RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
# RAZORPAY_KEY_SECRET=your_secret_key_here
```

```powershell
# 4. Initialize database
python -c "from utils.database_pg import init_postgresql; init_postgresql()"

# 5. Run the interactive demo
python demo_interactive_conversation.py
```

---

## 🏗️ System Architecture

### Multi-Agent Design Pattern

```
                    ┌─────────────────────────┐
                    │   Main Sales Agent      │
                    │  (Orchestrator + Chat)  │
                    └───────────┬─────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │ Recommendation│ │  Inventory │ │  Loyalty   │
        │     Agent     │ │   Agent    │ │   Agent    │
        └───────────────┘ └────────────┘ └────────────┘
                │               │               │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │   Payment    │ │ Fulfillment│ │Post-Purchase│
        │    Agent     │ │   Agent    │ │   Agent     │
        └──────────────┘ └────────────┘ └─────────────┘
```

### 6 Specialized AI Agents

| Agent | Purpose | Real-Time Capabilities |
|-------|---------|----------------------|
| 🎯 **Recommendation** | Product discovery & personalization | Purchase history analysis, seasonal promotions |
| 📦 **Inventory** | Stock & fulfillment | Live API integration (FakeStore, DummyJSON) |
| 🎁 **Loyalty & Rewards** | Discounts & points | Tier-based benefits, promo code validation |
| 💳 **Payment** | Transaction processing | Razorpay integration + mock gateway |
| 🚚 **Fulfillment** | Delivery & pickup | Express/standard shipping, tracking |
| 🌟 **Post-Purchase** | Support & returns | Reviews, exchanges, warranty claims |

---

## 🔗 Real-Time Integrations

### ✅ Active Integrations

#### 1. **Google Gemini AI** (gemini-2.0-flash-exp)
- **Status:** ✅ Active
- **Purpose:** Powers all 6 AI agents with natural language understanding
- **Cost:** Free tier available (60 requests/minute)
- **Setup:** Add `GEMINI_API_KEY` to `.env`

#### 2. **PostgreSQL Database** (Neon Cloud)
- **Status:** ✅ Active  
- **Purpose:** Customer profiles, orders, loyalty points, reviews
- **Cost:** Free tier: 0.5 GB storage, 1 database
- **Setup:** Get free database at [neon.tech](https://neon.tech)

#### 3. **Inventory APIs** (Free, No Auth Required)
- **Primary:** [FakeStore API](https://fakestoreapi.com) - 20 products
- **Fallback:** [DummyJSON](https://dummyjson.com) - 100+ products
- **Status:** ✅ Active
- **Cost:** 100% Free, no signup needed

#### 4. **Payment Gateway**
- **Mock Mode:** ✅ Active (default) - Free for testing
- **Razorpay Mode:** 🔄 Ready (requires API keys)
- **Cost:** Razorpay test mode is free, live mode: 2% transaction fee
- **Setup:** See [Razorpay Configuration](#razorpay-payment-gateway)

---

## 🛠️ Installation & Setup

### Step 1: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

**Required packages:**
```
google-adk>=0.1.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.9
requests>=2.31.0
razorpay>=1.4.2  # Optional
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```env
# ============================================
# REQUIRED: Google Gemini API
# ============================================
# Get your free API key: https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSyDhBHl-4gLgPB5A1kcjddLCSrh8-OWvUm0

# ============================================
# REQUIRED: PostgreSQL Database
# ============================================
# Option 1: Neon Cloud (Free) - https://neon.tech
DATABASE_URL=postgresql://username:password@host:5432/database

# Option 2: Local PostgreSQL
# DATABASE_URL=postgresql://localhost:5432/retail_db

# ============================================
# OPTIONAL: Razorpay Payment Gateway
# ============================================
# Get test keys: https://dashboard.razorpay.com/app/keys
# RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
# RAZORPAY_KEY_SECRET=your_secret_key_here
```

### Step 3: Initialize Database

```powershell
# Test PostgreSQL connection
python -c "from utils.database_pg import test_connection; test_connection()"

# Initialize database schema
python -c "from utils.database_pg import init_postgresql; init_postgresql()"
```

**Expected Output:**
```
✅ PostgreSQL connection successful!
✅ Database initialized with schema
✅ Sample data created
```

---

## 🎮 Running the System

### Option 1: Interactive Conversation Demo (Recommended)

Shows clear customer-agent dialogue for all 6 agents:

```powershell
python demo_interactive_conversation.py
```

**What you'll see:**
```
Customer: "I'm looking for electronics"
Agent: "I found 15 products in electronics. Here are the top recommendations..."

Customer: "Check stock for product XYZ"
Agent: "Great news! Product XYZ is in stock at 3 locations..."
```

### Option 2: Production System (Full Features)

```powershell
python run_production.py
```

**4 Available Modes:**
1. 🛒 **Complete Shopping Journey** - Full customer experience
2. ⚡ **Quick Multi-Agent Demo** - Rapid capability overview  
3. 💬 **Interactive Chat Mode** - Chat with individual agents
4. 🔧 **Test Real APIs** - Verify all API connections

```powershell
python demo_auto.py
```

---

## 🎯 Agent Capabilities

### 1. 🎯 Recommendation Agent

**Purpose:** Intelligent product discovery and personalization

**Capabilities:**
- ✅ Personalized recommendations based on purchase history
- ✅ Product search by category, brand, or keywords
- ✅ Bundle suggestions (e.g., laptop + mouse + bag)
- ✅ Seasonal promotions and deals
- ✅ Similar product recommendations

**Sample Conversation:**
```
Customer: "I'm looking for electronics for my home office"
Agent: "I found 12 products in our electronics category. Based on your 
       previous purchases of work accessories, I recommend:
       1. Ergonomic Wireless Mouse - $29.99 (20% off)
       2. USB-C Hub 7-in-1 - $49.99
       3. LED Desk Lamp - $34.99"
```

### 2. 📦 Inventory Agent

**Purpose:** Real-time stock management and fulfillment options

**Capabilities:**
- ✅ Live stock checking across all store locations
- ✅ Real-time product data from FakeStore API + DummyJSON
- ✅ Fulfillment options: ship to home, click & collect, in-store pickup
- ✅ Inventory reservation during checkout
- ✅ Alternative product suggestions if out of stock

**Sample Conversation:**
```
Customer: "Is the Wireless Mouse available near me?"
Agent: "Great news! The Ergonomic Wireless Mouse is in stock at:
       📍 Manhattan Store - 15 units (0.5 mi away)
       📍 Brooklyn Store - 8 units (3.2 mi away)
       📦 Online warehouse - 150+ units (2-day shipping)
       
       Would you like to reserve one for pickup or have it shipped?"
```

### 3. 🎁 Loyalty & Rewards Agent

**Purpose:** Maximize customer value with discounts and rewards

**Capabilities:**
- ✅ Loyalty tier management (Bronze, Silver, Gold, Platinum)
- ✅ Automatic discount application
- ✅ Promo code validation and stacking
- ✅ Points calculation and redemption
- ✅ Personalized offers based on tier

**Loyalty Tiers:**
| Tier | Discount | Free Shipping | Points Multiplier |
|------|----------|---------------|-------------------|
| Bronze | 5% | Orders >$50 | 1x |
| Silver | 10% | All orders | 1.5x |
| Gold | 15% | All orders | 2x |
| Platinum | 20% | All orders | 3x |

**Sample Conversation:**
```
Customer: "Do I have any discounts available?"
Agent: "Yes! You're a Gold member with these benefits:
       💎 15% automatic discount on all purchases
       🚚 Free shipping on every order
       ⭐ 2x points on every purchase
       🎁 Current points balance: 1,250 ($12.50 value)
       
       For your $49.99 mouse purchase:
       - Regular price: $49.99
       - Gold discount (15%): -$7.50
       - Final price: $42.49
       - Points earned: 85 points"
```

### 4. 💳 Payment Agent

**Purpose:** Secure payment processing with multiple options

**Capabilities:**
- ✅ Multiple payment methods (credit card, UPI, gift card, wallet)
- ✅ Razorpay payment gateway integration
- ✅ Saved payment methods
- ✅ Split payments (e.g., gift card + credit card)
- ✅ Payment retry handling
- ✅ Transaction verification

**Payment Options:**
- 💳 Credit/Debit Cards (Visa, Mastercard, Amex)
- 📱 UPI (Google Pay, PhonePe, Paytm)
- 🎁 Gift Cards & Store Credit
- 💰 Digital Wallets

**Sample Conversation:**
```
Customer: "I want to pay $30 with my gift card and the rest with my card"
Agent: "Perfect! Here's your payment breakdown:
       🎁 Gift card balance: $30.00
       💳 Credit card (Visa ****4242): $12.49
       ──────────────────────────
       Total amount: $42.49
       
       Processing payment... ✅ Payment successful!
       Transaction ID: TXN_123456789"
```

### 5. 🚚 Fulfillment Agent

**Purpose:** Flexible delivery and pickup coordination

**Capabilities:**
- ✅ Multiple delivery speeds (same-day, express, standard)
- ✅ In-store pickup scheduling
- ✅ Real-time shipment tracking
- ✅ Delivery time slot selection
- ✅ Store staff notifications
- ✅ Order modification before shipment

**Delivery Options:**
| Type | Speed | Cost | Tracking |
|------|-------|------|----------|
| Same-Day | 4-6 hours | $9.99 | Real-time GPS |
| Express | 1-2 days | $4.99 | Live updates |
| Standard | 3-5 days | Free | Daily updates |
| Pickup | 2 hours | Free | SMS notification |

**Sample Conversation:**
```
Customer: "How fast can I get this delivered to Brooklyn?"
Agent: "For delivery to Brooklyn, NY 11201:
       
       🚀 Same-Day Delivery - $9.99
          Delivered by 6 PM today (4 hours)
       
       ⚡ Express Delivery - $4.99
          Delivered tomorrow by 10 AM
       
       📦 Standard Delivery - FREE
          Delivered Dec 5-7 (3-5 business days)
       
       🏪 Click & Collect - FREE
          Ready for pickup in 2 hours at Brooklyn Store
       
       Which option works best for you?"
```

### 6. 🌟 Post-Purchase Support Agent

**Purpose:** Complete after-sales care and support

**Capabilities:**
- ✅ Easy returns and exchanges (30-day policy)
- ✅ Product review submission
- ✅ Order tracking and history
- ✅ Warranty claim processing
- ✅ Product troubleshooting support
- ✅ Replacement requests

**Sample Conversation:**
```
Customer: "I want to return the mouse I bought yesterday"
Agent: "I can help with that return. Let me pull up your order...
       
       📦 Order #ORD_789 - Ergonomic Wireless Mouse
       📅 Purchase date: Dec 1, 2024
       ✅ Eligible for return (within 30-day window)
       
       Return options:
       1. 🏪 In-store return (instant refund)
       2. 📬 Ship it back (pre-paid label)
       
       Reason for return? (helps us improve)
       - Defective/damaged
       - Changed my mind
       - Wrong product
       - Other"
```

---

## 📡 API Configuration

### Razorpay Payment Gateway

#### Free Test Mode Setup

1. **Create Razorpay Account** (Free)
   - Visit: https://dashboard.razorpay.com/signup
   - No credit card required for test mode

2. **Get Test API Keys**
   - Go to: https://dashboard.razorpay.com/app/keys
   - Click "Generate Test Key"
   - Copy both keys:
     - `rzp_test_xxxxxxxxxxxxxx` (Key ID)
     - `xxxxxxxxxxxxxxxxxxxxxxxx` (Secret)

3. **Update `.env` File**
   ```env
   # Uncomment and add your keys
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. **Restart Application**
   ```powershell
   python demo_interactive_conversation.py
   ```

**Test Card Details** (Use in test mode):
```
Card Number: 4111 1111 1111 1111
CVV: 123
Expiry: Any future date
Name: Any name
```

#### Razorpay Features Enabled

✅ Payment order creation  
✅ Payment verification  
✅ Automatic failure handling  
✅ Multiple payment methods (cards, UPI, wallets)  
✅ Test mode with mock transactions  

**Cost:**
- Test mode: 100% Free
- Live mode: 2% + GST per transaction
- No setup fees or monthly charges

### Inventory API Integration

**Current Setup:**
- **Primary:** FakeStore API (https://fakestoreapi.com)
  - 20 products across 4 categories
  - 100% Free, no authentication needed
  - Response time: < 200ms

- **Fallback:** DummyJSON (https://dummyjson.com)
  - 100+ products with detailed info
  - 100% Free, no authentication needed
  - Response time: < 300ms

**API Endpoints Used:**
```python
# FakeStore API
GET /products              # All products
GET /products/{id}         # Single product
GET /products/categories   # All categories
GET /products/category/{cat}  # Products by category

# DummyJSON
GET /products              # All products
GET /products/search?q={query}  # Search products
```

**No configuration needed** - APIs are pre-integrated and work out of the box!

---

## 💾 Database Setup

### Option 1: Neon Cloud PostgreSQL (Recommended - Free)

**Why Neon?**
- ✅ Free tier: 0.5 GB storage
- ✅ Serverless (auto-scales to zero)
- ✅ No credit card required
- ✅ Instant setup (2 minutes)

**Setup Steps:**

1. **Create Account**
   - Visit: https://neon.tech
   - Sign up with email/GitHub

2. **Create Database**
   - Click "Create Project"
   - Name: `retail_sales_db`
   - Region: Choose closest to you

3. **Copy Connection String**
   - Click "Connection Details"
   - Copy PostgreSQL connection string:
   ```
   postgresql://user:pass@host.region.aws.neon.tech:5432/dbname
   ```

4. **Update `.env`**
   ```env
   DATABASE_URL=postgresql://user:pass@host.region.aws.neon.tech:5432/dbname
   ```

5. **Initialize Database**
   ```powershell
   python -c "from utils.database_pg import init_postgresql; init_postgresql()"
   ```

### Option 2: Local PostgreSQL

1. **Install PostgreSQL**
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Default port: 5432

2. **Create Database**
   ```sql
   CREATE DATABASE retail_sales_db;
   ```

3. **Update `.env`**
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/retail_sales_db
   ```

4. **Initialize Schema**
   ```powershell
   python -c "from utils.database_pg import init_postgresql; init_postgresql()"
   ```

### Database Schema

**Tables Created:**
```sql
-- Customers
customers (
    customer_id, name, email, phone, 
    tier, points, created_at
)

-- Orders
orders (
    order_id, customer_id, total_amount,
    status, created_at
)

-- Order Items  
order_items (
    item_id, order_id, product_sku,
    quantity, price
)

-- Product Reviews
reviews (
    review_id, customer_id, product_sku,
    rating, comment, created_at
)

-- Returns
returns (
    return_id, order_id, reason,
    status, created_at
)
```

---

## 🧪 Testing & Validation

### Verify All Integrations

```powershell
# Test database connection
python -c "from utils.database_pg import test_connection; test_connection()"

# Test payment API
python -c "from utils.external_apis.payment_api import PaymentAPI; PaymentAPI().create_payment_order(100, 'INR', 'test')"

# Test inventory API
python -c "from utils.external_apis.inventory_api import get_products; print(len(get_products()))"

# Run full API test
python run_production.py
# Select option 4: Test Real APIs
```

**Expected Output:**
```
✅ Payment API: Connected (razorpay/mock_payment_gateway)
✅ Inventory API: Connected (FakeStore API)
✅ PostgreSQL: Connected
✅ Gemini API: Key configured
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. "Module not found" Error
```
Solution: Install dependencies
powershell: pip install -r requirements.txt
```

#### 2. "GEMINI_API_KEY not found"
```
Solution: Create .env file with your API key
.env: GEMINI_API_KEY=your_key_here
```

#### 3. "Database connection failed"
```
Solution: Check DATABASE_URL in .env
Test with: python -c "from utils.database_pg import test_connection; test_connection()"
```

#### 4. "Razorpay payment failed"
```
Solution: Ensure test mode is enabled or use mock mode
Remove RAZORPAY keys from .env to use mock gateway
```

#### 5. "Inventory API timeout"
```
Solution: Check internet connection
Fallback to DummyJSON will happen automatically
```

### Debug Mode

Enable detailed logging:
```powershell
$env:DEBUG="1"
python demo_interactive_conversation.py
```

---

## 📁 Project Structure

```
retail_sales_agent/
├── agents/
│   ├── sales_agent/
│   │   ├── __init__.py
│   │   └── sales_agent.py          # Main orchestrator
│   └── worker_agents/
│       ├── __init__.py
│       ├── recommendation_agent.py  # Product recommendations
│       ├── inventory_agent.py       # Stock management
│       ├── loyalty_agent.py         # Rewards & discounts
│       ├── payment_agent.py         # Payment processing
│       ├── fulfillment_agent.py     # Delivery & pickup
│       └── post_purchase_agent.py   # Returns & support
├── utils/
│   ├── database_pg.py              # PostgreSQL operations
│   ├── external_apis/
│   │   ├── payment_api.py          # Razorpay integration
│   │   └── inventory_api.py        # FakeStore/DummyJSON
│   └── tools/
│       ├── recommendation_tools.py
│       ├── inventory_tools.py
│       ├── loyalty_tools.py
│       ├── payment_tools.py
│       ├── fulfillment_tools.py
│       └── post_purchase_tools.py
├── config/
│   └── config.py                   # Environment config
├── .env                            # API keys & secrets
├── demo_interactive_conversation.py # Interactive demo
├── run_production.py               # Production system
├── demo_auto.py                    # Automated demo
├── main.py                         # Original demo
├── requirements.txt
└── README.md
```

---

## 🎓 Learning Resources

### Google Gemini AI
- API Documentation: https://ai.google.dev/docs
- Get API Key: https://aistudio.google.com/apikey
- Pricing: https://ai.google.dev/pricing

### Razorpay Payment Gateway
- Documentation: https://razorpay.com/docs/
- Test Mode Guide: https://razorpay.com/docs/payments/test-integration
- Dashboard: https://dashboard.razorpay.com/

### PostgreSQL & Neon
- Neon Docs: https://neon.tech/docs
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/

---

## 🚀 Next Steps

### For Development
1. ✅ Run `demo_interactive_conversation.py` to see all agents in action
2. ✅ Test with real Razorpay keys for payment integration
3. ✅ Customize agent responses in `worker_agents/` folder
4. ✅ Add more products via inventory APIs
5. ✅ Extend loyalty tiers and rewards logic

### For Production
1. Switch to Razorpay live mode keys
2. Use production PostgreSQL database
3. Add authentication & user management
4. Implement rate limiting
5. Add logging & monitoring
6. Deploy to cloud (AWS/Azure/GCP)

---

## 📞 Support

**Issues?**
- Check [Troubleshooting](#troubleshooting) section
- Review `.env` configuration
- Test each API individually

**Want to Extend?**
- Add new agents in `agents/worker_agents/`
- Create new tools in `utils/tools/`
- Modify conversation flows in agent files

---

## 📄 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ using Google Gemini AI, PostgreSQL, and Razorpay**
   - Submits product review

4. **Omnichannel Shopping Experience**
   - Customer continues from mobile app
   - Checks in-store pickup options
   - Uses personalized offers

5. **Interactive Chat Mode**
   - Free-form conversation with the agent
   - Test any scenario you want

### Example Conversation

```
👤 Customer: Hi! I'm looking for wireless headphones. I'm customer CUST1001

🤖 Sales Agent: Hello! I'd be happy to help you find the perfect wireless 
headphones. Let me check what we have available for you...

[Agent uses recommendation_agent to get personalized suggestions]

Based on your profile, I recommend:
• Wireless Bluetooth Headphones - $129.99 (4.5⭐, 234 reviews)
  Premium noise-canceling with 30-hour battery
• Sony WH-1000XM5 - $299.99 (4.8⭐, 892 reviews)

Would you like to know more about either of these?

👤 Customer: The first one sounds good. Is it in stock?

🤖 Sales Agent: Let me check availability for you...

[Agent uses inventory_agent]

Great news! The Wireless Bluetooth Headphones are in stock:
• Online Warehouse: 450 units available
• New York - 5th Avenue: 12 units available

Fulfillment options:
✓ Ship to home: 3-5 business days ($5.99, free for 3+ items)
✓ Click & collect: Ready in 2 hours at New York store (FREE)
✓ In-store: Available for immediate purchase

Which option would you prefer?
```

## 🗄️ Database

The system uses SQLite with synthetic data including:
- **10 customer profiles** with varying loyalty tiers
- **20+ products** across multiple categories
- **Real-time inventory** tracking across 5 store locations + online warehouse
- **Active promotions** and loyalty programs
- **Order history** and session management

Database is automatically created and populated on first run.

## 🔧 Configuration

Edit `config/config.py` to customize:
- Default AI model
- Loyalty tier thresholds
- Store locations
- Product categories
- Retry settings

## 📊 Agent Architecture

The system uses a **hierarchical multi-agent architecture**:

```
                    ┌─────────────────┐
                    │  Sales Agent    │
                    │ (Orchestrator)  │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
     ┌─────▼─────┐     ┌────▼────┐     ┌─────▼─────┐
     │Recommend  │     │Inventory│     │  Loyalty  │
     │  Agent    │     │  Agent  │     │   Agent   │
     └───────────┘     └─────────┘     └───────────┘
           │                 │                 │
     ┌─────▼─────┐     ┌────▼────┐     ┌─────▼─────┐
     │  Payment  │     │Fulfill  │     │Post-Purch │
     │   Agent   │     │  Agent  │     │   Agent   │
     └───────────┘     └─────────┘     └───────────┘
```

Each worker agent has specialized tools and knowledge for its domain.

## 🎓 Key Design Patterns

1. **Agent-as-Tool Pattern**: Worker agents are wrapped as tools for the main agent
2. **Stateless Tool Functions**: Each tool function is independent and testable
3. **Error Handling**: Tools return structured responses with status codes
4. **Session Continuity**: Context maintained across conversation turns
5. **Omnichannel Support**: Channel-agnostic conversation flow

## 🛠️ Extending the System

### Adding a New Product Category

Edit `utils/database.py` → `seed_products()` function

### Adding a New Worker Agent

1. Create agent file in `agents/worker_agents/`
2. Create tool functions in `utils/tools/`
3. Register agent in `agents/sales_agent/sales_agent.py`

### Adding New Promotions

Edit `utils/database.py` → `seed_promotions()` function

## 📝 API Key Security

**⚠️ Important Security Notes:**

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude `.env`
- Use environment variables in production
- Rotate API keys regularly

## 🔍 Troubleshooting

### "GEMINI_API_KEY not found"
Set your API key as an environment variable:
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

### "Module not found" errors
Ensure you're in the virtual environment and dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Database issues
Delete `data/retail_sales.db` and restart - it will be recreated automatically.

## 📚 Technologies Used

- **Google ADK** (Agent Development Kit)
- **Google Gemini 2.0** (LLM)
- **SQLite** (Database)
- **Python 3.8+**

## 🎯 Based On

This project architecture is inspired by the market purchase analyst agent from the provided notebook, adapted for retail sales with:
- Multiple specialized worker agents instead of a single agent
- Omnichannel conversation management
- Complete purchase flow orchestration
- Loyalty and post-purchase support

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs!

## 📧 Support

For issues or questions, please check:
1. This README
2. Code comments in each module
3. Google ADK documentation

---

**Built with ❤️ using Google's Agent Development Kit**

*Challenge: Retail [ABFRL] - Conversational Sales Agent*
