"""
Payment API Integration - Using free mock payment API
For production, replace with real Razorpay API
"""
import requests
import json
from datetime import datetime
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Free Payment Mock API - https://fakestoreapi.com for testing
# For real Razorpay, you'll need to sign up at https://razorpay.com/

class PaymentAPI:
    """Payment API wrapper supporting both mock and real Razorpay"""
    
    def __init__(self, use_real_api=False, razorpay_key_id=None, razorpay_key_secret=None):
        self.use_real_api = use_real_api
        self.razorpay_key_id = razorpay_key_id
        self.razorpay_key_secret = razorpay_key_secret
        
        if use_real_api and not (razorpay_key_id and razorpay_key_secret):
            print("⚠️  Warning: Real Razorpay API requested but credentials not provided")
            print("   Get free test credentials at: https://razorpay.com/")
            self.use_real_api = False
    
    def create_payment_order(self, amount, currency="INR", customer_id=None):
        """
        Create a payment order
        
        Args:
            amount: Amount in smallest currency unit (paise for INR)
            currency: Currency code (default: INR)
            customer_id: Customer identifier
            
        Returns:
            Dict with order details
        """
        if self.use_real_api:
            return self._create_razorpay_order(amount, currency)
        else:
            return self._create_mock_order(amount, currency, customer_id)
    
    def _create_razorpay_order(self, amount, currency):
        """Create order using real Razorpay API"""
        try:
            import razorpay
            client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
            
            order_data = {
                'amount': int(amount * 100),  # Convert to paise
                'currency': currency,
                'payment_capture': 1
            }
            
            order = client.order.create(data=order_data)
            
            return {
                "status": "success",
                "provider": "razorpay",
                "order_id": order['id'],
                "amount": amount,
                "currency": currency,
                "created_at": order['created_at'],
                "payment_url": f"https://api.razorpay.com/v1/checkout/{order['id']}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Razorpay API error: {str(e)}"
            }
    
    def _create_mock_order(self, amount, currency, customer_id):
        """Create mock payment order using free API"""
        # Using JSONPlaceholder as a free mock API
        order_id = f"PAY_{random.randint(100000, 999999)}"
        
        # Simulate API call
        mock_response = {
            "status": "success",
            "provider": "mock_payment_gateway",
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "customer_id": customer_id,
            "created_at": datetime.now().isoformat(),
            "payment_url": f"https://mock-payment.example.com/pay/{order_id}",
            "test_cards": {
                "success": "4111 1111 1111 1111",
                "failure": "4000 0000 0000 0002"
            }
        }
        
        return mock_response
    
    def verify_payment(self, order_id, payment_id, signature=None):
        """
        Verify payment completion
        
        Args:
            order_id: Order ID
            payment_id: Payment transaction ID
            signature: Payment signature (for Razorpay)
            
        Returns:
            Dict with verification status
        """
        if self.use_real_api:
            return self._verify_razorpay_payment(order_id, payment_id, signature)
        else:
            return self._verify_mock_payment(order_id, payment_id)
    
    def _verify_razorpay_payment(self, order_id, payment_id, signature):
        """Verify using real Razorpay API"""
        try:
            import razorpay
            client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
            
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            return {
                "status": "success",
                "verified": True,
                "payment_id": payment_id,
                "order_id": order_id
            }
        except Exception as e:
            return {
                "status": "error",
                "verified": False,
                "message": str(e)
            }
    
    def _verify_mock_payment(self, order_id, payment_id):
        """Verify mock payment"""
        # Simulate 95% success rate
        success = random.random() < 0.95
        
        return {
            "status": "success" if success else "failed",
            "verified": success,
            "payment_id": payment_id,
            "order_id": order_id,
            "transaction_id": f"TXN_{random.randint(100000000, 999999999)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_payment_status(self, payment_id):
        """Get payment status"""
        if self.use_real_api:
            return self._get_razorpay_status(payment_id)
        else:
            return self._get_mock_status(payment_id)
    
    def _get_razorpay_status(self, payment_id):
        """Get status from Razorpay"""
        try:
            import razorpay
            client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
            payment = client.payment.fetch(payment_id)
            
            return {
                "status": "success",
                "payment_id": payment_id,
                "payment_status": payment['status'],
                "amount": payment['amount'] / 100,
                "method": payment.get('method', 'unknown')
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _get_mock_status(self, payment_id):
        """Get mock payment status"""
        statuses = ["authorized", "captured", "processing"]
        
        return {
            "status": "success",
            "payment_id": payment_id,
            "payment_status": random.choice(statuses),
            "timestamp": datetime.now().isoformat()
        }

# Initialize payment API with environment variables
razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')

# Use real Razorpay if credentials are available
use_real_api = bool(razorpay_key_id and razorpay_key_secret)

if use_real_api:
    payment_api = PaymentAPI(
        use_real_api=True,
        razorpay_key_id=razorpay_key_id,
        razorpay_key_secret=razorpay_key_secret
    )
    print("✅ Payment API initialized (Razorpay - Real)")
    print(f"   Using Key ID: {razorpay_key_id[:15]}...")
else:
    payment_api = PaymentAPI(use_real_api=False)
    print("✅ Payment API initialized (Mock mode - Free)")
    print("   To use real Razorpay: Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env")
