# 🛒 Retail Sales Agent - AI Shopping Assistant

> **Multi-Agent AI System for Indian Retail Shopping with Google Gemini & Razorpay**

An intelligent retail assistant powered by **6 specialized AI agents** that work together seamlessly to provide a complete shopping experience from product discovery to checkout and post-purchase support.

---

## 🌟 What is This?

**Retail Sales Agent** is an AI-powered shopping assistant that uses **6 specialized agents** working together in perfect harmony. Instead of manually switching between different tools, you simply chat naturally, and the system automatically:

- 🎯 Recommends products based on your needs
- 📦 Checks real-time inventory across 5 Indian warehouse locations
- 🎁 Applies loyalty discounts and promo codes
- 💳 Processes payments via **Razorpay** (real payment links!)
- 🚚 Arranges delivery or store pickup
- 🌟 Handles returns, reviews, and support

**Example Conversation:**
```
You: I want running shoes under ₹5000

AI:  🎯 Found 5 perfect options!
     📦 All in stock at Mumbai, Delhi, Bengaluru warehouses
     🎁 You're Gold tier - 15% off applied!
     💳 Here's your Razorpay payment link: https://rzp.io/rzp/...
     🚚 Estimated delivery: 3-5 days
```

All in **one natural conversation** - no menus, no switching screens!

---

## ✨ Key Features

### 🤖 6 AI Agents Working Together

| Agent | What It Does |
|-------|--------------|
| **🎯 Recommendation** | Personalized product suggestions, bundles, seasonal deals |
| **📦 Inventory** | Real-time stock checking across 5 Indian warehouses |
| **🎁 Loyalty** | Automatic discounts (5%-20%), promo codes, points tracking |
| **💳 Payment** | Razorpay payment links, saved cards, UPI |
| **🚚 Fulfillment** | Same-day, express, standard delivery options |
| **🌟 Support** | Returns, exchanges, order tracking, reviews |

### 🔗 Real Integrations

- ✅ **Google Gemini 2.0** - AI brain powering all agents
- ✅ **Razorpay API** - Real payment links (test mode available)
- ✅ **PostgreSQL (Neon Cloud)** - Cloud database with 1200+ products
- ✅ **Indian Product Catalog** - 1200+ products across 12 categories
- ✅ **5 Indian Warehouses** - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad

### 📊 Database Overview

| Item | Count |
|------|-------|
| **Products** | 1,200+ |
| **Categories** | 12 |
| **Warehouses** | 5 |
| **Inventory Entries** | 6,000+ |
| **Customers** | 32 |

### 🏷️ Product Categories

| Category | Products | Price Range |
|----------|----------|-------------|
| Electronics | 100 | ₹2,999 - ₹79,999 |
| Home & Kitchen | 100 | ₹199 - ₹14,999 |
| Clothing - Men | 100 | ₹299 - ₹4,999 |
| Clothing - Women | 100 | ₹399 - ₹7,999 |
| Footwear | 100 | ₹299 - ₹7,999 |
| Beauty & Personal Care | 100 | ₹49 - ₹2,999 |
| Grocery & Gourmet | 100 | ₹29 - ₹1,499 |
| Sports & Fitness | 100 | ₹199 - ₹9,999 |
| Toys & Baby | 100 | ₹149 - ₹4,999 |
| Automotive | 100 | ₹149 - ₹14,999 |
| Mobile Accessories | 100 | ₹99 - ₹3,999 |
| Books & Stationery | 100 | ₹49 - ₹1,999 |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key ([Get free key](https://aistudio.google.com/apikey))
- Git (for cloning)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Vedag812/Retail-Agent.git
cd Retail-Agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your API keys:
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=your_postgresql_url_here
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### Run the App

```bash
python app.py
```

That's it! The chatbot will start and all 6 agents will coordinate automatically.

---

## 📖 How to Use

### Starting a Conversation

```bash
$ python app.py

🛒 RETAIL SALES AGENT v1.0
AI-Powered Shopping Assistant with 6 Agents

👋 Hi! I'm your AI Shopping Assistant.
💡 Try: 'I want running shoes under ₹5000' or 'Check my rewards'

👤 You: _
```

### Example Queries

**Product Search:**
```
"I want running shoes for marathons"
"Show me laptops under ₹50000"
"What sarees do you have?"
"Find organic honey"
```

**Check Inventory:**
```
"Is this available in Mumbai?"
"Do you have size 10 in stock?"
"What warehouses have this product?"
```

**Loyalty & Discounts:**
```
"Check my rewards balance"
"What's my loyalty tier?"
"Apply promo code DIWALI20"
```

**Checkout:**
```
"I'll buy this"
"Generate payment link"
"I've completed the payment"
```

**Post-Purchase:**
```
"Where's my order?"
"I want to return this"
"Write a review for my recent purchase"
```

---

## 🧪 Testing

### Run Automated E2E Test

```bash
python test_e2e_flow.py
```

This tests the complete flow:
1. ✅ Search products
2. ✅ Check inventory
3. ✅ Create Razorpay payment link
4. ✅ Confirm payment
5. ✅ Schedule delivery
6. ✅ Verify in database

### Sample Output:
```
======================================================================
  🛒 AUTOMATED E2E TEST - COMPLETE ORDER FLOW
======================================================================

👤 Customer: Neha Reddy (CUST2002)
📍 Location: Bengaluru, Karnataka

📍 STEP 1: SEARCH PRODUCTS
   🔍 Searching for: 'honey'
   ✅ Found 3 products

📍 STEP 3: CREATE PAYMENT LINK (Razorpay)
   📦 ORDER ID:      ORD257663
   💳 Payment Link:  https://rzp.io/rzp/2tcV8HA
   💰 Amount:        ₹1,998.00

📍 STEP 5: CONFIRM PAYMENT
   ✅ PAYMENT CONFIRMED!
   📊 Status: PAID

🎉 All steps completed successfully!
```

### Check Orders in Database

```bash
python check_orders.py
```

### Show All Products

```bash
python show_products.py
```

---

## 🛠️ Configuration

### Required: Gemini API Key

Get your free API key from [Google AI Studio](https://aistudio.google.com/apikey)

```env
GEMINI_API_KEY=your_key_here
```

### Required: PostgreSQL Database

Get free PostgreSQL from [Neon](https://neon.tech):

```env
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
```

### Optional: Razorpay Payments

Get test keys from [Razorpay Dashboard](https://dashboard.razorpay.com):

```env
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=your_secret
```

---

## 📁 Project Structure

```
retail_sales_agent/
├── app.py                    # 👈 START HERE - Main application
├── .env                      # API keys (create this)
├── requirements.txt          # Dependencies
│
├── agents/
│   ├── sales_agent/
│   │   └── sales_agent.py   # Main orchestrator with direct payment tools
│   └── worker_agents/       # 6 specialized agents
│       ├── recommendation_agent.py
│       ├── inventory_agent.py
│       ├── loyalty_agent.py
│       ├── payment_agent.py
│       ├── fulfillment_agent.py
│       └── post_purchase_agent.py
│
├── utils/
│   ├── db.py                # PostgreSQL connection (Neon Cloud)
│   ├── tools/               # Agent tool functions
│   │   ├── recommendation_tools.py
│   │   ├── inventory_tools.py
│   │   ├── payment_tools.py      # Razorpay integration
│   │   ├── fulfillment_tools.py
│   │   ├── loyalty_tools.py
│   │   └── post_purchase_tools.py
│   └── external_apis/
│       └── inventory_api.py      # FakeStore + DummyJSON
│
├── data/
│   ├── populate_1200_products.py # 1200+ Indian products
│   └── populate_india_dataset.py # Indian customers & inventory
│
├── config/
│   └── config.py            # Settings & configuration
│
└── tests/
    ├── test_e2e_flow.py     # End-to-end automated test
    ├── test_payment_flow.py  # Payment flow test
    └── check_orders.py       # View orders in database
```

---

## 💳 Payment Flow

### How Razorpay Integration Works

1. **Customer selects product** → Agent creates order in PostgreSQL
2. **Payment link generated** → Real Razorpay URL (e.g., `https://rzp.io/rzp/xxx`)
3. **Customer pays** → Click link, complete payment on Razorpay
4. **Confirm payment** → Agent updates order status to "PAID"
5. **Delivery scheduled** → Tracking ID generated

### Order Flow Diagram

```
Search → Select → Create Order → Payment Link → Pay → Confirm → Deliver
         ↓           ↓              ↓           ↓       ↓         ↓
       Agent    PostgreSQL      Razorpay    Customer   Agent   Tracking
```

---

## 🎓 How Agents Work Together

When you ask: **"I want running shoes under ₹5000"**

1. **Main Sales Agent** analyzes your request
2. **🎯 Recommendation Agent** finds suitable products from 1200+ catalog
3. **📦 Inventory Agent** checks stock across 5 Indian warehouses
4. **🎁 Loyalty Agent** applies your member discounts
5. **💳 Payment Agent** generates Razorpay payment link
6. **🚚 Fulfillment Agent** arranges delivery
7. **🌟 Support Agent** available for post-purchase help

All of this happens **automatically** in a natural conversation!

---

## 📊 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Google ADK** | Agent Development Kit |
| **Google Gemini 2.0 Flash** | AI Model |
| **PostgreSQL (Neon)** | Cloud Database |
| **Razorpay** | Payment Gateway |
| **Python 3.11+** | Runtime |
| **psycopg2** | PostgreSQL Driver |

---

## 🐛 Troubleshooting

**"GEMINI_API_KEY not found"**
- Create `.env` file in project root
- Add: `GEMINI_API_KEY=your_key`
- Get key from: https://aistudio.google.com/apikey

**"Database connection failed"**
- Check DATABASE_URL in .env
- Ensure Neon PostgreSQL is running
- Verify connection string format

**"Razorpay error"**
- Check RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
- Use test keys for development
- Verify keys from Razorpay dashboard

**"Module not found"**
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new agent in `agents/worker_agents/`
3. Add tools in `utils/tools/`
4. Register in `sales_agent.py`
5. Submit PR!

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects!

---

## 🌐 Links

- **GitHub**: https://github.com/Vedag812/Retail-Agent
- **Google Gemini**: https://ai.google.dev/
- **Razorpay**: https://razorpay.com/
- **Neon PostgreSQL**: https://neon.tech/

---

## 👏 Built With

- ❤️ Google Gemini AI
- 💳 Razorpay Payment Gateway
- 🐘 Neon PostgreSQL
- 🇮🇳 Indian Product Catalog (1200+ products)

---

**Ready to start?** Just run: `python app.py`
