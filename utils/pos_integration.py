"""
POS (Point of Sale) Integration Module
Simulates in-store terminal interactions for barcode scanning and payment processing
"""
import random
from datetime import datetime
import json

class POSTerminal:
    """Simulated POS Terminal for in-store interactions"""
    
    def __init__(self, store_location="New York - 5th Avenue", terminal_id=None):
        self.store_location = store_location
        self.terminal_id = terminal_id or f"POS-{random.randint(1000, 9999)}"
        self.current_cart = []
        self.session_id = None
        print(f"✅ POS Terminal initialized: {self.terminal_id} at {store_location}")
    
    def start_session(self, customer_id=None):
        """Start a new POS session"""
        self.session_id = f"SESSION-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.current_cart = []
        
        print(f"\n{'='*60}")
        print(f"🏪 POS SESSION STARTED")
        print(f"{'='*60}")
        print(f"Terminal: {self.terminal_id}")
        print(f"Location: {self.store_location}")
        print(f"Session: {self.session_id}")
        if customer_id:
            print(f"Customer: {customer_id}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "session_id": self.session_id,
            "terminal_id": self.terminal_id,
            "location": self.store_location
        }
    
    def scan_barcode(self, sku, quantity=1):
        """
        Simulate barcode scanning
        
        Args:
            sku: Product SKU/barcode
            quantity: Number of items scanned
        """
        print(f"🔍 BARCODE SCAN: {sku}")
        print(f"   Quantity: {quantity}")
        
        # Simulate barcode lookup (would call inventory_agent in real system)
        # For demo, we'll create a mock product
        product = {
            "sku": sku,
            "name": f"Product {sku}",
            "price": round(random.uniform(9.99, 299.99), 2),
            "quantity": quantity
        }
        
        # Add to cart
        self.current_cart.append(product)
        
        # Simulate beep sound
        print("   🔊 BEEP!")
        print(f"   ✅ Added to cart: {product['name']} x{quantity} @ ${product['price']:.2f}")
        
        subtotal = sum(item['price'] * item['quantity'] for item in self.current_cart)
        print(f"   💰 Cart Subtotal: ${subtotal:.2f}\n")
        
        return {
            "status": "success",
            "product": product,
            "cart_total": subtotal,
            "items_count": len(self.current_cart)
        }
    
    def scan_multiple(self, skus):
        """Scan multiple barcodes in sequence"""
        print(f"📦 Scanning {len(skus)} items...\n")
        results = []
        
        for sku in skus:
            result = self.scan_barcode(sku)
            results.append(result)
        
        return {
            "status": "success",
            "scanned_items": len(skus),
            "total": sum(r['cart_total'] for r in results if r['status'] == 'success')
        }
    
    def apply_discount(self, discount_code=None, loyalty_tier=None):
        """Apply discount or loyalty benefits"""
        if not self.current_cart:
            return {"status": "error", "message": "Cart is empty"}
        
        subtotal = sum(item['price'] * item['quantity'] for item in self.current_cart)
        discount_amount = 0
        discount_reason = ""
        
        # Loyalty tier discounts
        tier_discounts = {
            "bronze": 0.05,
            "silver": 0.10,
            "gold": 0.15,
            "platinum": 0.20
        }
        
        if loyalty_tier and loyalty_tier.lower() in tier_discounts:
            discount_pct = tier_discounts[loyalty_tier.lower()]
            discount_amount = subtotal * discount_pct
            discount_reason = f"{loyalty_tier.upper()} Member ({int(discount_pct*100)}% off)"
        
        # Promo codes
        elif discount_code:
            if discount_code == "SAVE20":
                discount_amount = 20.00
                discount_reason = "Promo Code: SAVE20"
            elif discount_code == "WELCOME10":
                discount_amount = subtotal * 0.10
                discount_reason = "Promo Code: WELCOME10 (10% off)"
        
        print(f"🎁 DISCOUNT APPLIED")
        print(f"   Reason: {discount_reason}")
        print(f"   Discount: -${discount_amount:.2f}")
        print(f"   New Total: ${subtotal - discount_amount:.2f}\n")
        
        return {
            "status": "success",
            "discount_amount": discount_amount,
            "discount_reason": discount_reason,
            "new_total": subtotal - discount_amount
        }
    
    def process_payment(self, payment_method="card", amount=None):
        """
        Process payment at POS terminal
        
        Args:
            payment_method: 'card', 'cash', 'mobile', 'gift_card'
            amount: Payment amount (auto-calculated if None)
        """
        if not self.current_cart:
            return {"status": "error", "message": "Cart is empty"}
        
        subtotal = sum(item['price'] * item['quantity'] for item in self.current_cart)
        tax = subtotal * 0.08  # 8% tax
        total = subtotal + tax
        
        if amount is None:
            amount = total
        
        print(f"\n{'='*60}")
        print(f"💳 PAYMENT PROCESSING")
        print(f"{'='*60}")
        print(f"Method: {payment_method.upper()}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (8%): ${tax:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"{'='*60}")
        
        # Simulate payment processing
        if payment_method == "card":
            print("💳 Insert/Tap card...")
            print("   Processing...")
            print("   ✅ PAYMENT APPROVED")
        elif payment_method == "cash":
            print(f"💵 Cash tendered: ${amount:.2f}")
            change = amount - total
            if change > 0:
                print(f"   💰 Change due: ${change:.2f}")
        elif payment_method == "mobile":
            print("📱 Scan QR code or tap phone...")
            print("   ✅ PAYMENT APPROVED")
        elif payment_method == "gift_card":
            print("🎁 Gift card scanned...")
            print("   ✅ PAYMENT APPROVED")
        
        transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100,999)}"
        
        print(f"\n   Transaction ID: {transaction_id}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "payment_method": payment_method,
            "amount": total,
            "subtotal": subtotal,
            "tax": tax,
            "session_id": self.session_id
        }
    
    def print_receipt(self):
        """Print receipt (simulated)"""
        if not self.current_cart:
            return {"status": "error", "message": "Cart is empty"}
        
        subtotal = sum(item['price'] * item['quantity'] for item in self.current_cart)
        tax = subtotal * 0.08
        total = subtotal + tax
        
        print(f"\n{'='*60}")
        print(f"              📄 RECEIPT")
        print(f"{'='*60}")
        print(f"Store: {self.store_location}")
        print(f"Terminal: {self.terminal_id}")
        print(f"Session: {self.session_id}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'-'*60}")
        
        for item in self.current_cart:
            item_total = item['price'] * item['quantity']
            print(f"{item['name']:<30} x{item['quantity']:>2}  ${item_total:>8.2f}")
        
        print(f"{'-'*60}")
        print(f"{'Subtotal:':<45} ${subtotal:>10.2f}")
        print(f"{'Tax (8%):':<45} ${tax:>10.2f}")
        print(f"{'='*60}")
        print(f"{'TOTAL:':<45} ${total:>10.2f}")
        print(f"{'='*60}")
        print(f"\n        Thank you for shopping with us!")
        print(f"               Visit again soon!")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "receipt_data": {
                "items": self.current_cart,
                "subtotal": subtotal,
                "tax": tax,
                "total": total
            }
        }
    
    def end_session(self):
        """End POS session and clear cart"""
        session = self.session_id
        items = len(self.current_cart)
        
        self.current_cart = []
        self.session_id = None
        
        print(f"✅ Session {session} ended ({items} items processed)\n")
        
        return {
            "status": "success",
            "session_id": session,
            "items_processed": items
        }


def demo_pos_workflow():
    """Demonstrate complete POS workflow"""
    print("\n" + "="*60)
    print("🏪 POS TERMINAL DEMO")
    print("="*60)
    
    # Initialize terminal
    pos = POSTerminal(store_location="New York - 5th Avenue")
    
    # Start session
    pos.start_session(customer_id="CUST1001")
    
    # Scan items
    print("📦 Customer brings items to checkout...\n")
    pos.scan_barcode("SKU1001")
    pos.scan_barcode("SKU1002", quantity=2)
    pos.scan_barcode("SKU1003")
    
    # Apply loyalty discount
    pos.apply_discount(loyalty_tier="platinum")
    
    # Process payment
    pos.process_payment(payment_method="card")
    
    # Print receipt
    pos.print_receipt()
    
    # End session
    pos.end_session()


if __name__ == "__main__":
    demo_pos_workflow()
