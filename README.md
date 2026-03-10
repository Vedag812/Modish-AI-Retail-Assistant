# Modish AI - Multi-Agent Retail Assistant

An AI shopping assistant where 6 specialized agents work together to handle a complete retail transaction. You talk to the system in natural language, and behind the scenes, different agents handle product search, inventory checks, payments, delivery, loyalty points, and post-purchase support.

Built this to learn Google's Agent Development Kit (ADK) and understand how multi-agent orchestration works in practice. The retail domain made sense because a shopping flow naturally breaks into distinct responsibilities.

## The agents

```
Sales Agent (orchestrator)
├── Recommendation Agent  → Suggests products based on what you ask for
├── Inventory Agent       → Checks stock availability and pricing
├── Payment Agent         → Handles checkout and payment processing
├── Fulfillment Agent     → Manages shipping and delivery tracking
├── Loyalty Agent         → Tracks reward points, applies discounts
└── Post-Purchase Agent   → Returns, exchanges, order status queries
```

The **Sales Agent** is the one you talk to. It figures out which worker agent to route your request to, collects the response, and gives you a unified answer. If your request touches multiple agents (e.g., "buy this red kurta and apply my loyalty points"), it orchestrates between them.

## Example conversation

```
You: "Show me cotton kurtas under 2000 rupees"
→ Recommendation Agent searches the product catalog
→ Inventory Agent checks stock for each suggestion
→ Sales Agent combines both and responds with available options

You: "Buy the blue one, use my reward points"
→ Inventory Agent reserves the item
→ Loyalty Agent calculates point redemption
→ Payment Agent processes the adjusted total
→ Fulfillment Agent creates a shipping order
```

## How I built it

The agents use **Google ADK** (Agent Development Kit) with **Gemini** as the underlying LLM. Each agent has:
- A system prompt defining its role and tools
- Python functions it can call (database queries, calculations, etc.)
- Clear boundaries on what it should and shouldn't handle

The product catalog uses an Indian retail dataset - kurtas, sarees, electronics, etc. with prices in INR.

## Tech

- **Agent framework**: Google ADK with InMemoryRunner
- **LLM**: Google Gemini API
- **Backend**: Python, Flask (api_server.py for the REST API)
- **Frontend**: React app (ey-frontend/)
- **Database**: SQLite with product catalog and order data
- **Deployment configs**: Railway, Render, Procfile

## Running it

```bash
# install dependencies
pip install -r requirements.txt

# set up env (needs a Google Gemini API key)
cp .env.example .env
# edit .env with your GOOGLE_API_KEY

# run the CLI version
python app.py

# or run the API server + frontend
python api_server.py
cd ey-frontend && npm install && npm start
```

## What's interesting about multi-agent systems

The tricky part isn't building individual agents - it's the orchestration. When should the sales agent delegate vs answer directly? How do you handle errors when one agent fails mid-transaction? What if two agents need the same data?

I ran into all of these. The payment agent failing after inventory was reserved was the hardest edge case - you need rollback logic that works across agents.
