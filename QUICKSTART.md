# 🚀 Quick Start Guide

## Step-by-Step Setup

### 1. Get Your Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 2. Set Up Environment

Open PowerShell in the project directory and run:

```powershell
# Set your API key
$env:GEMINI_API_KEY="AIzaSyDhBHl-4gLgPB5A1kcjddLCSrh8-OWvUm0"

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```powershell
python main.py
```

The system will:
- ✅ Initialize the database with synthetic data
- ✅ Create 10 customer profiles
- ✅ Populate 20+ products
- ✅ Set up inventory across 5 stores
- ✅ Load all 6 worker agents
- ✅ Start the interactive demo menu

### 4. Try a Demo Scenario

Select option **1** for a complete purchase flow:
- Product recommendations
- Inventory checking
- Loyalty discount application
- Payment processing
- Delivery scheduling

Or select option **5** for interactive chat mode!

## 🎯 Test Customer IDs

Use these pre-populated customer profiles:
- `CUST1001` - Gold tier customer
- `CUST1002` - Silver tier customer
- `CUST1003` - Bronze tier customer
- `CUST1004` - Platinum tier customer

## 💡 Sample Test Scenarios

### Scenario 1: Basic Purchase
```
Customer: Hi, I'm looking for headphones. I'm CUST1001
→ Agent provides recommendations
→ Customer asks about availability
→ Agent checks inventory
→ Customer proceeds to checkout
```

### Scenario 2: With Promo Code
```
Customer: Show me laptops for CUST1002
→ Get recommendations
Customer: I have promo code SAVE20
→ Apply discount
→ Complete purchase
```

### Scenario 3: Return Request
```
Customer: I need to return order ORD12345, I'm CUST1003
→ Initiate return
→ Track return status
```

## 🔧 Troubleshooting

### API Key Issues
If you see "GEMINI_API_KEY not found":
```powershell
# Check if it's set
$env:GEMINI_API_KEY

# Set it again
$env:GEMINI_API_KEY="your-key"
```

### Module Import Errors
```powershell
# Make sure you're in the project directory
cd c:\Users\VEDANT\retail_sales_agent

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Reset
If you want to reset the database:
```powershell
# Delete the database file
Remove-Item .\data\retail_sales.db

# Run main.py again - it will recreate
python main.py
```

## 📊 What's Included

- **1 Main Sales Agent** (orchestrator)
- **6 Worker Agents** (specialized)
- **30+ Tool Functions** (capabilities)
- **10 Customer Profiles** (with history)
- **20+ Products** (across categories)
- **5 Store Locations** (with inventory)
- **4 Active Promotions** (promo codes)
- **5 Demo Scenarios** (ready to test)

## 🎓 Architecture Overview

```
Main Sales Agent
    ├── Recommendation Agent (product suggestions)
    ├── Inventory Agent (stock checking)
    ├── Loyalty Agent (discounts & offers)
    ├── Payment Agent (payment processing)
    ├── Fulfillment Agent (delivery & pickup)
    └── Post-Purchase Agent (returns & support)
```

Each agent has specialized tools and coordinates with others to provide a seamless shopping experience!

## ✨ Key Features Demonstrated

✅ Multi-agent orchestration  
✅ Natural conversation flow  
✅ Context maintenance across turns  
✅ Personalized recommendations  
✅ Real-time inventory checking  
✅ Loyalty program integration  
✅ Multiple payment methods  
✅ Omnichannel fulfillment  
✅ Post-purchase support  
✅ Error handling & recovery  

---

**Ready to Start? Run:** `python main.py`
