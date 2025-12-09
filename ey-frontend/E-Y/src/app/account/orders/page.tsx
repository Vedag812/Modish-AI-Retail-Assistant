'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useCustomer } from '@/context/customer-context';
import { useFirestore } from '@/firebase';
import { collection, query, where, orderBy, getDocs } from 'firebase/firestore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';
import Link from 'next/link';
import Image from 'next/image';
import { 
  Package, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Truck,
  ShoppingBag,
  ArrowRight,
  RefreshCw,
  CreditCard
} from 'lucide-react';

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
  paymentStatus: 'pending' | 'completed' | 'failed';
  orderStatus?: 'processing' | 'shipped' | 'delivered' | 'cancelled';
}

function OrderSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-48" />
        <Skeleton className="h-4 w-32" />
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
        </div>
      </CardContent>
    </Card>
  );
}

function getStatusBadge(status: string) {
  switch (status) {
    case 'completed':
    case 'delivered':
      return <Badge className="bg-green-500"><CheckCircle className="h-3 w-3 mr-1" />Completed</Badge>;
    case 'pending':
    case 'processing':
      return <Badge className="bg-yellow-500"><Clock className="h-3 w-3 mr-1" />Processing</Badge>;
    case 'shipped':
      return <Badge className="bg-blue-500"><Truck className="h-3 w-3 mr-1" />Shipped</Badge>;
    case 'failed':
    case 'cancelled':
      return <Badge variant="destructive"><XCircle className="h-3 w-3 mr-1" />Failed</Badge>;
    default:
      return <Badge variant="secondary">{status}</Badge>;
  }
}

export default function OrdersPage() {
  const { customer, isLoading: isCustomerLoading, isAuthenticated } = useCustomer();
  const firestore = useFirestore();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const orderId = searchParams.get('order_id');
  const paymentSuccess = searchParams.get('payment_success');

  useEffect(() => {
    if (!isCustomerLoading && !isAuthenticated) {
      router.push('/login?redirect=/account/orders');
    }
  }, [isAuthenticated, isCustomerLoading, router]);

  useEffect(() => {
    const fetchOrders = async () => {
      if (!customer || !firestore) return;

      try {
        const ordersRef = collection(firestore, 'orders');
        const q = query(
          ordersRef,
          where('customerId', '==', customer.customer_id),
          orderBy('createdAt', 'desc')
        );
        
        const snapshot = await getDocs(q);
        const ordersData = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        })) as Order[];
        
        setOrders(ordersData);
      } catch (error) {
        console.error('Error fetching orders:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (customer && firestore) {
      fetchOrders();
    }
  }, [customer, firestore]);

  if (isCustomerLoading || !isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-8 space-y-6">
        <Skeleton className="h-10 w-48" />
        <OrderSkeleton />
        <OrderSkeleton />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">My Orders</h1>
          <p className="text-muted-foreground">Track and manage your orders</p>
        </div>
        <Button asChild>
          <Link href="/products">
            <ShoppingBag className="h-4 w-4 mr-2" />
            Continue Shopping
          </Link>
        </Button>
      </div>

      {/* Success banner if redirected after payment */}
      {orderId && (
        <Card className="mb-8 bg-green-500/10 border-green-500/30">
          <CardContent className="py-4">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-green-500/20 flex items-center justify-center">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-green-600">Order Placed Successfully!</h3>
                <p className="text-sm text-muted-foreground">
                  Order ID: {orderId}. You'll receive a confirmation email shortly.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="space-y-6">
          <OrderSkeleton />
          <OrderSkeleton />
        </div>
      ) : orders.length === 0 ? (
        <Card className="text-center py-16">
          <CardContent>
            <Package className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
            <h2 className="text-xl font-semibold mb-2">No orders yet</h2>
            <p className="text-muted-foreground mb-6">
              Start shopping to see your orders here!
            </p>
            <Button asChild>
              <Link href="/products">Browse Products</Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <Card key={order.id}>
              <CardHeader className="pb-4">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div>
                    <CardTitle className="text-lg">Order #{order.id.slice(-8).toUpperCase()}</CardTitle>
                    <CardDescription>
                      Placed on {new Date(order.createdAt.seconds * 1000).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    {getStatusBadge(order.paymentStatus)}
                    {order.orderStatus && getStatusBadge(order.orderStatus)}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Order Items */}
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
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{item.name}</p>
                        <p className="text-xs text-muted-foreground">
                          Qty: {item.quantity} {item.sku && `• SKU: ${item.sku}`}
                        </p>
                      </div>
                      <p className="font-medium text-sm">₹{(item.price * item.quantity).toLocaleString('en-IN')}</p>
                    </div>
                  ))}
                </div>

                <Separator />

                {/* Order Summary */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-1 text-sm">
                    <p><span className="text-muted-foreground">Payment:</span> {order.paymentMethod === 'cod' ? 'Cash on Delivery' : 'Razorpay'}</p>
                    <p><span className="text-muted-foreground">Shipping to:</span> {order.shippingAddress.city}, {order.shippingAddress.state}</p>
                    {order.pointsEarned > 0 && (
                      <p className="text-green-600">+{order.pointsEarned} loyalty points earned</p>
                    )}
                  </div>
                  <div className="text-right space-y-1">
                    <p className="text-sm text-muted-foreground">
                      Subtotal: ₹{order.subtotal.toLocaleString('en-IN')}
                    </p>
                    {order.loyaltyDiscount > 0 && (
                      <p className="text-sm text-green-600">
                        Loyalty Discount: -₹{order.loyaltyDiscount.toLocaleString('en-IN')}
                      </p>
                    )}
                    {order.couponDiscount > 0 && (
                      <p className="text-sm text-green-600">
                        Coupon ({order.couponCode}): -₹{order.couponDiscount.toLocaleString('en-IN')}
                      </p>
                    )}
                    <p className="font-bold text-lg">
                      Total: ₹{order.total.toLocaleString('en-IN')}
                    </p>
                  </div>
                </div>

                {/* Actions */}
                {order.paymentStatus === 'failed' && (
                  <div className="flex justify-end gap-2 pt-2">
                    <Button variant="outline" asChild>
                      <Link href="/checkout">
                        <RefreshCw className="h-4 w-4 mr-2" />
                        Retry Payment
                      </Link>
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
