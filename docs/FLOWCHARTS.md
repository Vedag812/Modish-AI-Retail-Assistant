# 📊 System Flowcharts - Retail Sales Agent

## 1. High-Level System Architecture

```mermaid
flowchart TB
    subgraph Frontend["🖥️ Frontend (Next.js - Vercel)"]
        UI[Web Interface]
        Chat[Chatbot Page]
        Products[Products Page]
        Cart[Shopping Cart]
        Checkout[Checkout Page]
    end

    subgraph Backend["⚙️ Backend (FastAPI - Render)"]
        API[REST API Server]
        SA[Sales Agent<br/>Orchestrator]
        
        subgraph Workers["Worker Agents"]
            RA[Recommendation<br/>Agent]
            IA[Inventory<br/>Agent]
            PA[Payment<br/>Agent]
            LA[Loyalty<br/>Agent]
            FA[Fulfillment<br/>Agent]
            PPA[Post-Purchase<br/>Agent]
        end
    end

    subgraph External["☁️ External Services"]
        Firebase[(Firebase<br/>Firestore)]
        Gemini[Google Gemini<br/>2.0 AI]
        Razorpay[Razorpay<br/>Payments]
    end

    UI --> API
    Chat --> API
    Products --> API
    Cart --> API
    Checkout --> API

    API --> SA
    SA --> RA
    SA --> IA
    SA --> PA
    SA --> LA
    SA --> FA
    SA --> PPA

    SA --> Gemini
    RA --> Firebase
    IA --> Firebase
    PA --> Razorpay
    LA --> Firebase
    FA --> Firebase
    PPA --> Firebase
```

---

## 2. User Journey Flowchart

```mermaid
flowchart TD
    Start([User Visits Website]) --> Landing[Landing Page]
    Landing --> |Browse| Products[View Products]
    Landing --> |Chat| Chatbot[Open Chatbot]
    
    Products --> |Filter/Search| Search[Search Products]
    Products --> |View Details| PDP[Product Detail Page]
    PDP --> |Add to Cart| Cart[Shopping Cart]
    
    Chatbot --> |Ask Question| AI{AI Processes<br/>Query}
    AI --> |Product Query| Recommend[Show Recommendations]
    AI --> |Order Query| OrderStatus[Show Order Status]
    AI --> |General Query| Response[AI Response]
    
    Recommend --> Cart
    
    Cart --> |Update Qty| Cart
    Cart --> |Remove Item| Cart
    Cart --> |Proceed| Auth{Logged In?}
    
    Auth --> |No| Login[Login/Signup]
    Auth --> |Yes| Checkout[Checkout Page]
    Login --> Checkout
    
    Checkout --> |Enter Details| Address[Add Address]
    Address --> Payment[Payment]
    Payment --> |Razorpay| Processing{Payment<br/>Processing}
    
    Processing --> |Success| Confirm[Order Confirmation]
    Processing --> |Failed| Payment
    
    Confirm --> |Track| Tracking[Order Tracking]
    Confirm --> End([Continue Shopping])
```

---

## 3. AI Agent Workflow

```mermaid
flowchart TD
    User[User Message] --> Sales[Sales Agent<br/>Orchestrator]
    
    Sales --> Analyze{Analyze<br/>Intent}
    
    Analyze --> |Product Search| R1[Recommendation Agent]
    Analyze --> |Stock Check| R2[Inventory Agent]
    Analyze --> |Payment Help| R3[Payment Agent]
    Analyze --> |Points/Rewards| R4[Loyalty Agent]
    Analyze --> |Shipping/Delivery| R5[Fulfillment Agent]
    Analyze --> |Returns/Support| R6[Post-Purchase Agent]
    
    R1 --> |Search Products| DB1[(Firestore)]
    R2 --> |Check Stock| DB2[(Firestore)]
    R3 --> |Process Payment| RP[Razorpay API]
    R4 --> |Get Points| DB3[(Firestore)]
    R5 --> |Track Order| DB4[(Firestore)]
    R6 --> |Handle Returns| DB5[(Firestore)]
    
    DB1 --> Compose[Compose Response]
    DB2 --> Compose
    RP --> Compose
    DB3 --> Compose
    DB4 --> Compose
    DB5 --> Compose
    
    Compose --> Gemini[Gemini AI<br/>Format Response]
    Gemini --> Response[Send to User]
```

---

## 4. Checkout Flow

```mermaid
flowchart TD
    Cart[Shopping Cart] --> Review[Review Items]
    Review --> Login{User<br/>Logged In?}
    
    Login --> |No| Auth[Login/Signup]
    Auth --> Customer[Load Customer Data]
    Login --> |Yes| Customer
    
    Customer --> Loyalty{Has Loyalty<br/>Points?}
    Loyalty --> |Yes| ApplyPoints[Show Points Option]
    Loyalty --> |No| Address
    ApplyPoints --> Address[Enter/Select Address]
    
    Address --> Promo{Apply Promo<br/>Code?}
    Promo --> |Yes| ValidatePromo{Valid?}
    ValidatePromo --> |Yes| ApplyDiscount[Apply Discount]
    ValidatePromo --> |No| Error[Show Error]
    Error --> Promo
    Promo --> |No| Summary
    ApplyDiscount --> Summary[Order Summary]
    
    Summary --> PayMethod{Payment<br/>Method}
    
    PayMethod --> |Razorpay| RazorpayInit[Initialize Razorpay]
    RazorpayInit --> RazorpayModal[Razorpay Modal]
    RazorpayModal --> PayResult{Payment<br/>Result}
    
    PayResult --> |Success| CreateOrder[Create Order in DB]
    PayResult --> |Failed| PayFailed[Show Error]
    PayFailed --> PayMethod
    
    CreateOrder --> UpdateInventory[Update Inventory]
    UpdateInventory --> AddPoints[Add Loyalty Points]
    AddPoints --> SendEmail[Send Confirmation]
    SendEmail --> Confirmation[Order Confirmation Page]
```

---

## 5. Data Flow Diagram

```mermaid
flowchart LR
    subgraph Client["Client Side"]
        Browser[Browser]
        LocalStorage[Local Storage<br/>Cart Data]
    end

    subgraph Server["Server Side"]
        FastAPI[FastAPI Server]
        Sessions[Session Store]
    end

    subgraph Database["Database Layer"]
        Firestore[(Firestore)]
        Products[Products<br/>Collection]
        Customers[Customers<br/>Collection]
        Orders[Orders<br/>Collection]
        Inventory[Inventory<br/>Collection]
    end

    subgraph AI["AI Layer"]
        Gemini[Gemini 2.0]
        Agents[Multi-Agent<br/>System]
    end

    Browser <--> |HTTP/REST| FastAPI
    Browser <--> LocalStorage
    FastAPI <--> Sessions
    FastAPI <--> Firestore
    Firestore --- Products
    Firestore --- Customers
    Firestore --- Orders
    Firestore --- Inventory
    FastAPI <--> Agents
    Agents <--> Gemini
```

---

## 6. Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API Server
    participant DB as Firestore

    U->>F: Enter Email
    F->>A: POST /api/auth/login
    A->>DB: Query customers by email
    
    alt Customer Found
        DB-->>A: Customer Data
        A-->>F: Success + Customer Info
        F->>F: Store in Context
        F-->>U: Redirect to Home
    else Not Found
        DB-->>A: Empty Result
        A-->>F: 404 Not Found
        F-->>U: Show Signup Option
    end

    U->>F: Fill Signup Form
    F->>A: POST /api/auth/register
    A->>DB: Create Customer Doc
    DB-->>A: Success
    A-->>F: New Customer Data
    F-->>U: Welcome Message
```

---

## 7. Product Search Flow

```mermaid
flowchart TD
    Query[User Search Query] --> Parse[Parse Query]
    Parse --> Type{Query Type}
    
    Type --> |Category| CatSearch[Category Filter]
    Type --> |Keyword| KeySearch[Keyword Search]
    Type --> |Price Range| PriceSearch[Price Filter]
    Type --> |Brand| BrandSearch[Brand Filter]
    
    CatSearch --> Combine[Combine Filters]
    KeySearch --> Combine
    PriceSearch --> Combine
    BrandSearch --> Combine
    
    Combine --> Firestore[(Query Firestore)]
    Firestore --> Results[Product Results]
    
    Results --> Sort{Sort By}
    Sort --> |Price Low| SortPrice1[Ascending]
    Sort --> |Price High| SortPrice2[Descending]
    Sort --> |Rating| SortRating[By Rating]
    Sort --> |Newest| SortNew[By Date]
    
    SortPrice1 --> Display[Display Products]
    SortPrice2 --> Display
    SortRating --> Display
    SortNew --> Display
```

---

## 8. Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Cart: Add Items
    Cart --> Checkout: Proceed
    Checkout --> PaymentPending: Submit Order
    PaymentPending --> PaymentFailed: Payment Failed
    PaymentFailed --> PaymentPending: Retry
    PaymentPending --> Confirmed: Payment Success
    Confirmed --> Processing: Order Received
    Processing --> Shipped: Dispatched
    Shipped --> OutForDelivery: Near Destination
    OutForDelivery --> Delivered: Delivered
    Delivered --> [*]
    
    Confirmed --> Cancelled: User Cancels
    Processing --> Cancelled: User Cancels
    Cancelled --> Refunded: Refund Initiated
    Refunded --> [*]
    
    Delivered --> ReturnRequested: Return Request
    ReturnRequested --> ReturnApproved: Approved
    ReturnApproved --> Returned: Item Received
    Returned --> Refunded
```

---

## 9. Cart Optimizer Logic

```mermaid
flowchart TD
    Cart[Cart Items] --> Calculate[Calculate Total]
    Calculate --> Checks{Run Checks}
    
    Checks --> FS{Total < ₹999?}
    FS --> |Yes| FSMsg[Show: Add ₹X for free shipping]
    FS --> |No| FSQualified[Show: Free shipping qualified!]
    
    Checks --> LP{Has Loyalty<br/>Points?}
    LP --> |Yes| LPMsg[Show: Use X points for ₹Y off]
    LP --> |No| LPEarn[Show: Earn X points on order]
    
    Checks --> Promo{Best Promo<br/>Available?}
    Promo --> |Yes| PromoMsg[Show: Apply CODE for ₹X off]
    Promo --> |No| NextPromo{Next Tier<br/>Promo?}
    NextPromo --> |Yes| NextMsg[Show: Add ₹X to unlock CODE]
    
    Checks --> Bundle{Multiple<br/>Items?}
    Bundle --> |Yes, ≥2| BundleMsg[Show: Bundle discount available]
    
    FSMsg --> Suggest[Display Suggestions]
    FSQualified --> Suggest
    LPMsg --> Suggest
    LPEarn --> Suggest
    PromoMsg --> Suggest
    NextMsg --> Suggest
    BundleMsg --> Suggest
    
    Suggest --> TotalSavings[Calculate Total Savings]
    TotalSavings --> Display[Show Optimizer Card]
```

---

## 10. Component Hierarchy

```mermaid
flowchart TD
    App[App Layout]
    
    App --> Header[Header]
    App --> Main[Main Content]
    App --> Footer[Footer]
    
    Header --> Logo[Logo]
    Header --> Nav[Navigation]
    Header --> Search[Search Bar]
    Header --> CartIcon[Cart Icon]
    Header --> UserMenu[User Menu]
    
    Main --> Routes{Routes}
    
    Routes --> Home[Home Page]
    Routes --> ProductList[Products Page]
    Routes --> ProductDetail[Product Detail]
    Routes --> CartPage[Cart Page]
    Routes --> CheckoutPage[Checkout]
    Routes --> ChatbotPage[Chatbot]
    Routes --> OrderConfirm[Order Confirmation]
    
    Home --> Hero[Hero Section]
    Home --> Featured[Featured Products]
    Home --> Categories[Category Grid]
    
    ProductList --> Filters[Filter Sidebar]
    ProductList --> Grid[Product Grid]
    ProductList --> Pagination[Pagination]
    
    ChatbotPage --> MessageList[Message List]
    ChatbotPage --> InputArea[Input Area]
    ChatbotPage --> QuickReplies[Quick Reply Buttons]
    
    CartPage --> CartItems[Cart Items List]
    CartPage --> CartOptimizer[Cart Optimizer]
    CartPage --> OrderSummary[Order Summary]
```

---

## How to View These Diagrams

1. **GitHub**: Push to GitHub - diagrams render automatically
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Online**: Use [mermaid.live](https://mermaid.live) to edit/export

---

*Generated for Retail Sales Agent Project*
