# 🏆 EY Techathon - Retail Sales AI Agent
## Presentation Diagrams

---

# SLIDE 1: System Architecture

```mermaid
flowchart LR
    subgraph User["👤 Customer"]
        Web[Web App]
    end

    subgraph AI["🤖 AI Layer"]
        Agent[Multi-Agent<br/>Orchestrator]
    end

    subgraph Services["☁️ Cloud Services"]
        direction TB
        Firebase[(Firebase)]
        Gemini[Gemini 2.0]
        Razorpay[Razorpay]
    end

    Web -->|Chat/Browse| Agent
    Agent -->|NLP| Gemini
    Agent -->|Data| Firebase
    Agent -->|Payments| Razorpay
    Agent -->|Response| Web
```

**Tech Stack:** Next.js • FastAPI • Google Gemini 2.0 • Firebase • Razorpay

---

# SLIDE 2: AI Agent Architecture

```mermaid
flowchart TB
    User[👤 Customer Query] --> Orchestrator[🧠 Sales Agent<br/>Orchestrator]
    
    Orchestrator --> A1[📦 Recommendation]
    Orchestrator --> A2[📊 Inventory]
    Orchestrator --> A3[💳 Payment]
    Orchestrator --> A4[🎁 Loyalty]
    Orchestrator --> A5[🚚 Fulfillment]
    Orchestrator --> A6[🔄 Post-Purchase]
    
    A1 --> Response[💬 AI Response]
    A2 --> Response
    A3 --> Response
    A4 --> Response
    A5 --> Response
    A6 --> Response
```

**6 Specialized Agents** powered by Google Gemini 2.0

---

# SLIDE 3: User Journey

```mermaid
flowchart LR
    A[🏠 Visit] --> B[🔍 Browse/Chat]
    B --> C[🛒 Add to Cart]
    C --> D[💳 Checkout]
    D --> E[✅ Order Confirmed]
    E --> F[📦 Track & Support]
```

**Seamless End-to-End Shopping Experience**

---

# SLIDE 4: Key Features Flow

```mermaid
flowchart TB
    subgraph Features["✨ Smart Features"]
        F1[🤖 AI Chatbot]
        F2[📍 Location Detection]
        F3[💰 Cart Optimizer]
        F4[🎁 Loyalty Program]
    end

    F1 --> |"Product Search<br/>Order Tracking<br/>Recommendations"| Value1[Personalized Shopping]
    F2 --> |"Nearest Store<br/>Delivery Estimates"| Value2[Local Experience]
    F3 --> |"Promo Codes<br/>Bundle Deals"| Value3[Maximum Savings]
    F4 --> |"Points & Tiers<br/>Exclusive Offers"| Value4[Customer Retention]
```

---

# SLIDE 5: Data Flow

```mermaid
flowchart LR
    A[📱 Frontend<br/>Next.js] <-->|REST API| B[⚙️ Backend<br/>FastAPI]
    B <-->|Firestore| C[(🗄️ Database<br/>Firebase)]
    B <-->|AI| D[🧠 Gemini 2.0]
    B <-->|Payments| E[💳 Razorpay]
```

---

# WIREFRAME SLIDES

## SLIDE 6: Main Screens Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           📱 RETAIL SALES AGENT                             │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│                 │                 │                 │                     │
│   🏠 HOME       │  🛍️ PRODUCTS    │  🤖 CHATBOT     │  🛒 CART           │
│                 │                 │                 │                     │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────────┐ │
│  │  Banner   │  │  │ Filters   │  │  │   AI 🤖   │  │  │ Items List    │ │
│  ├───────────┤  │  ├───────────┤  │  │  Message  │  │  ├───────────────┤ │
│  │ Category  │  │  │ Product   │  │  ├───────────┤  │  │ Smart Savings │ │
│  │   Grid    │  │  │   Grid    │  │  │  User 👤  │  │  ├───────────────┤ │
│  ├───────────┤  │  │           │  │  │  Message  │  │  │    Summary    │ │
│  │ Trending  │  │  │           │  │  ├───────────┤  │  ├───────────────┤ │
│  │ Products  │  │  │           │  │  │ [Type...] │  │  │  [Checkout]   │ │
│  └───────────┘  │  └───────────┘  │  └───────────┘  │  └───────────────┘ │
│                 │                 │                 │                     │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────┘
```

---

## SLIDE 7: Chatbot Interface

```
┌───────────────────────────────────────┐
│  🤖 RetailStore AI Assistant          │
├───────────────────────────────────────┤
│                                       │
│  ┌─────────────────────────────────┐  │
│  │ 🤖 Hello! How can I help you?  │  │
│  │    • Find products             │  │
│  │    • Track orders              │  │
│  │    • Get recommendations       │  │
│  └─────────────────────────────────┘  │
│                                       │
│              ┌─────────────────────┐  │
│              │ 👤 Show me TVs     │  │
│              │    under ₹50,000   │  │
│              └─────────────────────┘  │
│                                       │
│  ┌─────────────────────────────────┐  │
│  │ 🤖 Here are top TVs for you:   │  │
│  │    1. Samsung 55" - ₹45,999    │  │
│  │    2. LG 50" - ₹38,999         │  │
│  │    [Add to Cart]               │  │
│  └─────────────────────────────────┘  │
│                                       │
│  [📺 TVs] [👗 Fashion] [📦 Orders]   │
│  ┌─────────────────────────────────┐  │
│  │ Type your message...     [Send] │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

---

## SLIDE 8: Checkout Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        💳 CHECKOUT FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐ │
│    │   🛒    │     │   📍    │     │   💳    │     │   ✅    │ │
│    │  Cart   │ ──▶ │ Address │ ──▶ │ Payment │ ──▶ │ Confirm │ │
│    │ Review  │     │  Entry  │     │Razorpay │     │  Order  │ │
│    └─────────┘     └─────────┘     └─────────┘     └─────────┘ │
│                                                                 │
│    ✓ Smart Savings    ✓ Auto-fill      ✓ Secure      ✓ Tracking│
│    ✓ Promo Codes      ✓ Location       ✓ UPI/Card    ✓ Points  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SLIDE 9: Smart Features

```
┌─────────────────────────────────────────────────────────────────┐
│                     ✨ SMART FEATURES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────┐              │
│  │ 📍 LOCATION      │        │ 💡 CART OPTIMIZER │              │
│  │                  │        │                  │              │
│  │ Auto-detect city │        │ Smart savings    │              │
│  │ Nearest store    │        │ Promo codes      │              │
│  │ Delivery time    │        │ Loyalty points   │              │
│  └──────────────────┘        └──────────────────┘              │
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────┐              │
│  │ 🤖 AI CHATBOT    │        │ 🎁 LOYALTY       │              │
│  │                  │        │                  │              │
│  │ Natural language │        │ Bronze→Platinum  │              │
│  │ Product search   │        │ Points earning   │              │
│  │ Order tracking   │        │ Exclusive offers │              │
│  └──────────────────┘        └──────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SLIDE 10: Complete Solution Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🛒 RETAIL SALES AI AGENT                                 │
│                    ━━━━━━━━━━━━━━━━━━━━━━━━                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐          │
│   │  FRONTEND   │         │   BACKEND   │         │  SERVICES   │          │
│   │             │         │             │         │             │          │
│   │  Next.js    │◀───────▶│  FastAPI    │◀───────▶│  Firebase   │          │
│   │  React      │   REST  │  Python     │         │  Gemini 2.0 │          │
│   │  Tailwind   │   API   │  6 Agents   │         │  Razorpay   │          │
│   └─────────────┘         └─────────────┘         └─────────────┘          │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      ✨ KEY DIFFERENTIATORS                         │  │
│   │                                                                     │  │
│   │  🤖 Multi-Agent AI    📍 Smart Location    💰 Cart Optimizer       │  │
│   │  🎁 Loyalty Program   🚀 Real-time Chat    💳 Secure Payments      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# Quick Reference - Mermaid Code for Slides

Copy these into your presentation tool that supports Mermaid (or use mermaid.live to export as images):

## Architecture (Horizontal - fits slide better)
```
flowchart LR
    A[👤 User] --> B[📱 Next.js]
    B --> C[⚙️ FastAPI]
    C --> D[🧠 Gemini 2.0]
    C --> E[(Firebase)]
    C --> F[💳 Razorpay]
```

## Agent Flow (Compact)
```
flowchart TB
    Q[Query] --> O[Orchestrator]
    O --> R[Recommend] & I[Inventory] & P[Payment] & L[Loyalty]
    R & I & P & L --> Res[Response]
```

## User Journey (Linear)
```
flowchart LR
    A[Visit] --> B[Browse] --> C[Cart] --> D[Pay] --> E[Track]
```

---

*Created for EY Techathon 2025*
