"""
Web UI for Retail Sales Agent System
Flask-based interface with real-time chat
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import asyncio
import secrets
from datetime import datetime
from google.adk.runners import InMemoryRunner
from agents.worker_agents.recommendation_agent import recommendation_agent
from agents.worker_agents.inventory_agent import inventory_agent
from agents.worker_agents.loyalty_agent import loyalty_agent
from agents.worker_agents.payment_agent import payment_agent
from agents.worker_agents.fulfillment_agent import fulfillment_agent
from agents.worker_agents.post_purchase_agent import post_purchase_agent
from utils.external_apis.payment_api import payment_api
from utils.external_apis.inventory_api import InventoryAPI
import os
from io import StringIO
import sys

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

inventory_api = InventoryAPI()

# Agent configurations
AGENTS = {
    'recommendation': {
        'name': 'Recommendation Agent',
        'icon': '🎯',
        'agent': recommendation_agent,
        'description': 'Product discovery & personalization'
    },
    'inventory': {
        'name': 'Inventory Agent',
        'icon': '📦',
        'agent': inventory_agent,
        'description': 'Stock checking & availability'
    },
    'loyalty': {
        'name': 'Loyalty Agent',
        'icon': '🎁',
        'agent': loyalty_agent,
        'description': 'Rewards & discounts'
    },
    'payment': {
        'name': 'Payment Agent',
        'icon': '💳',
        'agent': payment_agent,
        'description': 'Secure payment processing'
    },
    'fulfillment': {
        'name': 'Fulfillment Agent',
        'icon': '🚚',
        'agent': fulfillment_agent,
        'description': 'Delivery & pickup options'
    },
    'support': {
        'name': 'Support Agent',
        'icon': '🌟',
        'agent': post_purchase_agent,
        'description': 'Returns & customer service'
    }
}

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', agents=AGENTS)

@app.route('/api/status')
def api_status():
    """Get system status"""
    return jsonify({
        'status': 'online',
        'integrations': {
            'gemini': bool(os.getenv('GEMINI_API_KEY')),
            'razorpay': payment_api.use_real_api,
            'database': bool(os.getenv('DATABASE_URL')),
            'inventory': True
        },
        'razorpay_mode': 'real' if payment_api.use_real_api else 'mock'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    agent_id = data.get('agent')
    message = data.get('message')
    
    if agent_id not in AGENTS:
        return jsonify({'error': 'Invalid agent'}), 400
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        # Run agent asynchronously
        agent_config = AGENTS[agent_id]
        response = asyncio.run(run_agent(agent_config['agent'], message))
        
        return jsonify({
            'success': True,
            'agent': agent_config['name'],
            'icon': agent_config['icon'],
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

async def run_agent(agent, message):
    """Run agent and capture output"""
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        runner = InMemoryRunner(agent=agent)
        await runner.run_debug(message)
        
        # Get captured output
        output = captured_output.getvalue()
        sys.stdout = old_stdout
        
        # Parse the output to extract agent response
        lines = output.split('\n')
        response_lines = []
        capture = False
        
        for line in lines:
            if '>' in line and not line.startswith('User >'):
                capture = True
                # Extract message after agent name
                parts = line.split('>', 1)
                if len(parts) > 1:
                    response_lines.append(parts[1].strip())
            elif capture and line.strip() and not line.startswith('Warning:'):
                response_lines.append(line.strip())
        
        response = '\n'.join(response_lines) if response_lines else output
        return response.strip() or "Agent processed your request successfully."
        
    except Exception as e:
        sys.stdout = old_stdout
        raise e

@app.route('/api/products')
def get_products():
    """Get product catalog"""
    try:
        products = inventory_api.get_products(limit=20)
        return jsonify({
            'success': True,
            'products': products
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    """Create payment order"""
    data = request.json
    amount = data.get('amount', 100)
    currency = data.get('currency', 'INR')
    customer_id = data.get('customer_id', 'GUEST')
    
    try:
        order = payment_api.create_payment_order(amount, currency, customer_id)
        return jsonify({
            'success': True,
            'order': order
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 RETAIL SALES AGENT - WEB UI")
    print("="*60)
    print("\n✅ Initializing system...")
    print(f"   🤖 AI: Google Gemini")
    print(f"   💳 Payments: {'Razorpay (Real)' if payment_api.use_real_api else 'Mock Gateway'}")
    print(f"   📦 Inventory: FakeStore API + DummyJSON")
    print(f"   🗄️  Database: PostgreSQL")
    print("\n🌐 Starting web server...")
    print(f"   URL: http://localhost:5000")
    print("\n👉 Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
