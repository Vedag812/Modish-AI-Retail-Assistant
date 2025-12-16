'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useCustomer } from '@/context/customer-context';
import { useFirestore } from '@/firebase';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { useToast } from '@/hooks/use-toast';
import Link from 'next/link';
import Image from 'next/image';
import { 
  CheckCircle, 
  Package, 
  Truck, 
  Crown,
  Gift,
  ShoppingBag,
  MessageCircle,
  ArrowRight,
  RefreshCw,
  XCircle,
  Loader2
} from 'lucide-react';

// Declare Razorpay on window for TypeScript
declare global {
  interface Window {
    Razorpay: any;
  }
}

interface OrderItem {
  productId: string;
  sku?: string;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

interface Order {
  id: string;
  customerId: string;
  customerName: string;
  customerEmail: string;
  createdAt: { seconds: number };
  items: OrderItem[];
  subtotal: number;
  loyaltyDiscount: number;
  couponDiscount: number;
  couponCode?: string;
  shippingCost: number;
  total: number;
  pointsEarned: number;
  shippingAddress: {
    fullName: string;
    phone: string;
    address: string;
    city: string;
    state: string;
    zipCode: string;
  };
  paymentMethod: string;
  paymentStatus: 'pending' | 'completed' | 'failed' | 'paid';
}

function OrderConfirmationContent() {
  const { customer, isAuthenticated } = useCustomer();
  const firestore = useFirestore();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRetrying, setIsRetrying] = useState(false);
  const [status, setStatus] = useState<'success' | 'failed' | 'pending'>('pending');

  const orderId = searchParams.get('order_id');
  const paymentStatus = searchParams.get('status');

  useEffect(() => {
    // Determine status from URL params
    if (paymentStatus === 'success' || paymentStatus === 'completed') {
      setStatus('success');
    } else if (paymentStatus === 'failed' || paymentStatus === 'cancelled') {
      setStatus('failed');
    } else {
      setStatus('pending');
    }
  }, [paymentStatus]);

  useEffect(() => {
    const fetchOrder = async () => {
      if (!orderId || !firestore) {
        setIsLoading(false);
        return;
      }

      try {
        const orderRef = doc(firestore, 'orders', orderId);
        const orderSnap = await getDoc(orderRef);
        
        if (orderSnap.exists()) {
          setOrder({
            id: orderSnap.id,
            ...orderSnap.data()
          } as Order);
        }
      } catch (error) {
        console.error('Error fetching order:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrder();
  }, [orderId, firestore]);

  // Retry payment function
  const handleRetryPayment = async () => {
    if (!order || !firestore || !customer) return;
    
    setIsRetrying(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    try {
      // Create new Razorpay order
      const response = await fetch(`${API_URL}/api/payment/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          customer_id: customer.customer_id,
          amount: order.total,
          description: `Retry payment for Order ${order.id.slice(-8).toUpperCase()}`,
          receipt: order.id
        }),
      });

      if (!response.ok) throw new Error('Failed to create payment order.');
      
      const orderData = await response.json();
      
      if (orderData.status === 'success' && orderData.order_id) {
        // Open Razorpay Checkout popup
        const options = {
          key: orderData.key_id,
          amount: orderData.amount * 100,
          currency: "INR",
          name: "Retail Store",
          description: `Order ${order.id.slice(-8).toUpperCase()}`,
          order_id: orderData.order_id,
          prefill: {
            name: customer.name,
            email: customer.email,
            contact: customer.phone || order.shippingAddress?.phone
          },
          notes: {
            order_id: order.id,
            customer_id: customer.customer_id
          },
          theme: {
            color: "#3399cc"
          },
          handler: async function (response: { razorpay_payment_id: string; razorpay_order_id: string; razorpay_signature: string }) {
            try {
              // Update order status in Firestore
              await updateDoc(doc(firestore, 'orders', order.id), {
                paymentStatus: 'paid',
                razorpayPaymentId: response.razorpay_payment_id,
                razorpayOrderId: response.razorpay_order_id,
              });
              
              toast({ title: "🎉 Payment Successful!", description: "Your order has been confirmed." });
              setStatus('success');
              router.replace(`/order-confirmation?order_id=${order.id}&status=success`);
            } catch (err) {
              console.error("Payment update error:", err);
              setStatus('success');
            }
          },
          modal: {
            ondismiss: function() {
              setIsRetrying(false);
              toast({ variant: "destructive", title: "Payment Cancelled", description: "You can try again anytime." });
            }
          }
        };

        const razorpay = new window.Razorpay(options);
        
        razorpay.on('payment.failed', function (response: any) {
          console.error("Payment failed:", response.error);
          setIsRetrying(false);
          toast({ 
            variant: "destructive", 
            title: "Payment Failed", 
            description: response.error.description || "Please try again."
          });
        });
        
        razorpay.open();
      } else {
        throw new Error(orderData.message || 'Failed to create payment order');
      }
    } catch (error: any) {
      console.error("Retry error:", error);
      toast({ variant: "destructive", title: "Error", description: error.message || "Could not initiate payment. Please try again." });
      setIsRetrying(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-16 max-w-2xl">
        <div className="text-center space-y-4">
          <Skeleton className="h-20 w-20 rounded-full mx-auto" />
          <Skeleton className="h-8 w-64 mx-auto" />
          <Skeleton className="h-4 w-48 mx-auto" />
        </div>
      </div>
    );
  }

  // Failed Payment
  if (status === 'failed') {
    return (
      <div className="container mx-auto px-4 py-16 max-w-2xl">
        <Card className="text-center">
          <CardContent className="py-12">
            <div className="h-20 w-20 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mx-auto mb-6">
              <XCircle className="h-10 w-10 text-red-600" />
            </div>
            <h1 className="text-3xl font-bold mb-2">Payment Failed</h1>
            <p className="text-muted-foreground mb-4">
              We couldn't process your payment. Please try again.
            </p>
            
            {order && (
              <div className="mb-8 p-4 bg-muted/50 rounded-lg text-left max-w-sm mx-auto">
                <p className="text-sm"><span className="text-muted-foreground">Order ID:</span> <span className="font-mono">{order.id.slice(-8).toUpperCase()}</span></p>
                <p className="text-sm"><span className="text-muted-foreground">Amount:</span> <span className="font-semibold">₹{order.total?.toLocaleString()}</span></p>
                <p className="text-sm"><span className="text-muted-foreground">Items:</span> {order.items?.length || 0} item(s)</p>
              </div>
            )}
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {order && customer ? (
                <Button size="lg" onClick={handleRetryPayment} disabled={isRetrying}>
                  {isRetrying ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Retry Payment (₹{order.total?.toLocaleString()})
                    </>
                  )}
                </Button>
              ) : (
                <Button asChild size="lg">
                  <Link href="/checkout">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Go to Checkout
                  </Link>
                </Button>
              )}
              <Button variant="outline" asChild size="lg">
                <Link href="/products">
                  <ShoppingBag className="h-4 w-4 mr-2" />
                  Continue Shopping
                </Link>
              </Button>
            </div>

            <div className="mt-8 p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                Having trouble? Contact our support via{' '}
                <Link href="/chatbot" className="text-primary hover:underline">
                  AI Assistant
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Success
  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      {/* Success Header */}
      <Card className="text-center mb-8 overflow-hidden">
        <div className="bg-gradient-to-r from-green-500 to-emerald-500 py-8">
          <div className="h-20 w-20 rounded-full bg-white flex items-center justify-center mx-auto mb-4 shadow-lg">
            <CheckCircle className="h-12 w-12 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Order Confirmed!</h1>
          <p className="text-green-100">
            Thank you for shopping with us, {customer?.name || 'Customer'}!
          </p>
        </div>
        <CardContent className="py-6">
          {orderId && (
            <p className="text-lg">
              Order ID: <span className="font-mono font-bold">{orderId.slice(-8).toUpperCase()}</span>
            </p>
          )}
          <p className="text-muted-foreground text-sm mt-1">
            A confirmation email has been sent to {customer?.email}
          </p>
        </CardContent>
      </Card>

      {/* Order Details */}
      {order && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="h-5 w-5" />
              Order Summary
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Items */}
            <div className="space-y-3">
              {order.items.map((item, idx) => (
                <div key={idx} className="flex items-center gap-4">
                  <div className="relative h-16 w-16 rounded-lg overflow-hidden border bg-muted flex-shrink-0">
                    {item.image ? (
                      <Image src={item.image} alt={item.name} fill className="object-contain p-1" />
                    ) : (
                      <div className="flex items-center justify-center h-full">
                        <Package className="h-6 w-6 text-muted-foreground" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium">{item.name}</p>
                    <p className="text-sm text-muted-foreground">Qty: {item.quantity}</p>
                  </div>
                  <p className="font-medium">₹{(item.price * item.quantity).toLocaleString('en-IN')}</p>
                </div>
              ))}
            </div>

            <Separator />

            {/* Pricing */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Subtotal</span>
                <span>₹{order.subtotal.toLocaleString('en-IN')}</span>
              </div>
              {order.loyaltyDiscount > 0 && (
                <div className="flex justify-between text-green-600">
                  <span>Loyalty Discount</span>
                  <span>-₹{order.loyaltyDiscount.toLocaleString('en-IN')}</span>
                </div>
              )}
              {order.couponDiscount > 0 && (
                <div className="flex justify-between text-green-600">
                  <span>Coupon ({order.couponCode})</span>
                  <span>-₹{order.couponDiscount.toLocaleString('en-IN')}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-muted-foreground">Shipping</span>
                <span>{order.shippingCost === 0 ? 'FREE' : `₹${order.shippingCost}`}</span>
              </div>
              <Separator />
              <div className="flex justify-between text-lg font-bold">
                <span>Total Paid</span>
                <span>₹{order.total.toLocaleString('en-IN')}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Loyalty Points Earned */}
      {order && order.pointsEarned > 0 && (
        <Card className="mb-8 bg-gradient-to-r from-yellow-500/10 to-amber-500/10 border-yellow-500/30">
          <CardContent className="py-4">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-yellow-500/20 flex items-center justify-center">
                <Crown className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <p className="font-semibold text-yellow-600">
                  +{order.pointsEarned} Loyalty Points Earned! 🎉
                </p>
                <p className="text-sm text-muted-foreground">
                  Your new balance: {((customer?.loyalty_points || 0) + order.pointsEarned).toLocaleString()} points
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Delivery Info */}
      {order && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Truck className="h-5 w-5" />
              Delivery Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Shipping To</p>
                <p className="font-medium">{order.shippingAddress.fullName}</p>
                <p className="text-sm text-muted-foreground">
                  {order.shippingAddress.address}<br />
                  {order.shippingAddress.city}, {order.shippingAddress.state} {order.shippingAddress.zipCode}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Phone: {order.shippingAddress.phone}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Expected Delivery</p>
                <p className="font-medium">
                  {new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toLocaleDateString('en-IN', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long'
                  })}
                </p>
                <p className="text-sm text-muted-foreground">
                  3-5 business days
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Button asChild size="lg">
          <Link href="/account/orders">
            <Package className="h-4 w-4 mr-2" />
            View All Orders
          </Link>
        </Button>
        <Button variant="outline" asChild size="lg">
          <Link href="/products">
            <ShoppingBag className="h-4 w-4 mr-2" />
            Continue Shopping
          </Link>
        </Button>
        <Button variant="outline" asChild size="lg">
          <Link href="/chatbot">
            <MessageCircle className="h-4 w-4 mr-2" />
            Need Help?
          </Link>
        </Button>
      </div>
    </div>
  );
}

export default function OrderConfirmationPage() {
  return (
    <Suspense fallback={<div className="container mx-auto px-4 py-8 text-center">Loading order...</div>}>
      <OrderConfirmationContent />
    </Suspense>
  );
}
