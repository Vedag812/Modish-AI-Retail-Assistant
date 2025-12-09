
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useFirestore } from '@/firebase';
import { useCart } from '@/hooks/use-cart';
import { useToast } from '@/hooks/use-toast';
import { useCustomer } from '@/context/customer-context';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { cn } from '@/lib/utils';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import Image from 'next/image';
import Link from 'next/link';
import { CheckCircle, TicketPercent, CreditCard, Banknote, Crown, Gift, Sparkles, Loader2 } from 'lucide-react';

// Address form schema
const addressSchema = z.object({
    fullName: z.string().min(2, 'Name is required'),
    phone: z.string().min(10, 'Valid phone number required'),
    address: z.string().min(5, 'Address is required'),
    city: z.string().min(2, 'City is required'),
    state: z.string().min(2, 'State is required'),
    zipCode: z.string().min(6, 'Valid PIN code required'),
});

type AddressFormValues = z.infer<typeof addressSchema>;

// Coupon data with loyalty tier requirements
const validCoupons: Record<string, { 
    description: string; 
    type: 'percentage' | 'flat'; 
    value: number;
    minOrder: number;
    forNewUsers?: boolean;
    loyaltyTier?: string[];
}> = {
    'WELCOME50': { description: "₹50 off for new customers", type: 'flat', value: 50, minOrder: 0, forNewUsers: true },
    'NEWUSER15': { description: "15% off for new customers", type: 'percentage', value: 15, minOrder: 500, forNewUsers: true },
    'SALE20': { description: "Get 20% off on your order", type: 'percentage', value: 20, minOrder: 1000 },
    'GET100': { description: "Get flat ₹100 off", type: 'flat', value: 100, minOrder: 500 },
    'GOLD10': { description: "10% off for Gold members", type: 'percentage', value: 10, minOrder: 0, loyaltyTier: ['Gold', 'Platinum'] },
    'PLATINUM15': { description: "15% off for Platinum members", type: 'percentage', value: 15, minOrder: 0, loyaltyTier: ['Platinum'] },
    'FESTIVE100': { description: "Flat ₹100 off - Festival Special", type: 'flat', value: 100, minOrder: 2000 },
};

// Loyalty tier benefits
const loyaltyBenefits: Record<string, { discount: number; freeShipping: boolean; pointsMultiplier: number }> = {
    'Bronze': { discount: 0, freeShipping: false, pointsMultiplier: 1 },
    'Silver': { discount: 5, freeShipping: false, pointsMultiplier: 1.5 },
    'Gold': { discount: 10, freeShipping: true, pointsMultiplier: 2 },
    'Platinum': { discount: 15, freeShipping: true, pointsMultiplier: 3 },
};

function CheckoutSkeleton() {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-12">
            <div className="space-y-8">
                <Skeleton className="h-48 w-full" />
                <Skeleton className="h-64 w-full" />
            </div>
            <div className="space-y-8">
                <Skeleton className="h-40 w-full" />
                <Skeleton className="h-64 w-full" />
            </div>
        </div>
      </div>
    );
}

export default function CheckoutPage() {
  const { customer, isLoading: isCustomerLoading, isAuthenticated } = useCustomer();
  const firestore = useFirestore();
  const router = useRouter();
  const { items, totalPrice, totalItems, clearCart } = useCart();
  const { toast } = useToast();
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [appliedCoupon, setAppliedCoupon] = useState('');
  const [couponDiscount, setCouponDiscount] = useState(0);
  const [paymentMethod, setPaymentMethod] = useState('razorpay');

  const addressForm = useForm<AddressFormValues>({
    resolver: zodResolver(addressSchema),
    defaultValues: {
      fullName: customer?.name || '',
      phone: customer?.phone || '',
      address: '',
      city: customer?.location?.split(',')[0]?.trim() || '',
      state: customer?.location?.split(',')[1]?.trim() || '',
      zipCode: '',
    },
  });

  // Update form when customer loads
  useEffect(() => {
    if (customer) {
      addressForm.setValue('fullName', customer.name || '');
      addressForm.setValue('phone', customer.phone || '');
      if (customer.location) {
        const parts = customer.location.split(',');
        addressForm.setValue('city', parts[0]?.trim() || '');
        addressForm.setValue('state', parts[1]?.trim() || '');
      }
    }
  }, [customer, addressForm]);

  // Redirect if not logged in
  useEffect(() => {
    if (!isCustomerLoading && !isAuthenticated) {
      toast({ title: 'Please Sign In', description: 'Sign in to proceed to checkout.', variant: 'destructive' });
      router.push('/login?redirect=/checkout');
    }
  }, [isAuthenticated, isCustomerLoading, router, toast]);

  // Calculate loyalty discount
  const loyaltyTier = customer?.loyalty_tier || 'Bronze';
  const loyaltyBenefit = loyaltyBenefits[loyaltyTier] || loyaltyBenefits['Bronze'];
  const loyaltyDiscount = (totalPrice * loyaltyBenefit.discount) / 100;
  
  // Shipping cost (free for Gold/Platinum)
  const baseShippingCost = 49;
  const shippingCost = loyaltyBenefit.freeShipping ? 0 : baseShippingCost;
  
  // Calculate totals
  const subtotalAfterLoyalty = totalPrice - loyaltyDiscount;
  const subtotalAfterCoupon = subtotalAfterLoyalty - couponDiscount;
  const finalTotal = Math.max(0, subtotalAfterCoupon + shippingCost);

  // Points to be earned
  const pointsToEarn = Math.floor(finalTotal * loyaltyBenefit.pointsMultiplier);

  // Check if customer is new (less than 200 points means likely new)
  const isNewCustomer = (customer?.loyalty_points || 0) < 200;

  // Get available coupons for this customer
  const getAvailableCoupons = () => {
    return Object.entries(validCoupons).filter(([code, coupon]) => {
      // Check minimum order
      if (totalPrice < coupon.minOrder) return false;
      
      // Check if it's for new users only
      if (coupon.forNewUsers && !isNewCustomer) return false;
      
      // Check loyalty tier requirement
      if (coupon.loyaltyTier && !coupon.loyaltyTier.includes(loyaltyTier)) return false;
      
      return true;
    });
  };

  const availableCoupons = getAvailableCoupons();

  const applyCoupon = (code: string) => {
    const coupon = validCoupons[code.toUpperCase()];
    if (!coupon) {
      toast({ variant: 'destructive', title: 'Invalid Coupon', description: 'This coupon code is not valid.' });
      return;
    }

    // Check if coupon is applicable
    if (totalPrice < coupon.minOrder) {
      toast({ variant: 'destructive', title: 'Minimum Order Required', description: `This coupon requires a minimum order of ₹${coupon.minOrder}.` });
      return;
    }

    if (coupon.forNewUsers && !isNewCustomer) {
      toast({ variant: 'destructive', title: 'Not Applicable', description: 'This coupon is only for new customers.' });
      return;
    }

    if (coupon.loyaltyTier && !coupon.loyaltyTier.includes(loyaltyTier)) {
      toast({ variant: 'destructive', title: 'Not Applicable', description: `This coupon is only for ${coupon.loyaltyTier.join('/')} members.` });
      return;
    }

    let discountValue = 0;
    if (coupon.type === 'percentage') {
      discountValue = (subtotalAfterLoyalty * coupon.value) / 100;
    } else {
      discountValue = coupon.value;
    }

    setCouponDiscount(discountValue);
    setAppliedCoupon(code.toUpperCase());
    toast({ title: "🎉 Coupon Applied!", description: `You saved ₹${discountValue.toFixed(2)}!` });
  };

  const removeCoupon = () => {
    setCouponDiscount(0);
    setAppliedCoupon('');
  };

  // Declare Razorpay on window for TypeScript
  declare global {
    interface Window {
      Razorpay: any;
    }
  }

  const handlePlaceOrder = async (addressData: AddressFormValues) => {
    if (!customer || !firestore || items.length === 0) {
      toast({ variant: 'destructive', title: "Error", description: "Please ensure your cart is not empty." });
      return;
    }
    
    setIsProcessing(true);
    
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    try {
      if (paymentMethod === 'razorpay') {
        // First save order to Firestore with pending status
        const orderRef = await addDoc(collection(firestore, 'orders'), {
          customerId: customer.customer_id,
          customerEmail: customer.email,
          customerName: customer.name,
          createdAt: serverTimestamp(),
          items: items,
          subtotal: totalPrice,
          loyaltyDiscount,
          couponDiscount,
          couponCode: appliedCoupon || null,
          shippingCost,
          total: finalTotal,
          pointsEarned: pointsToEarn,
          shippingAddress: addressData,
          paymentMethod: 'razorpay',
          paymentStatus: 'pending',
        });

        // Try to create Razorpay order via backend for inline checkout
        let useInlineCheckout = false;
        let orderData: any = null;
        
        try {
          const response = await fetch(`${API_URL}/api/payment/create-order`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              customer_id: customer.customer_id,
              amount: finalTotal,
              description: `Order with ${items.length} items`,
              receipt: orderRef.id
            }),
          });

          if (response.ok) {
            orderData = await response.json();
            if (orderData.status === 'success' && orderData.order_id && orderData.key_id) {
              useInlineCheckout = true;
            }
          }
        } catch (err) {
          console.log('Inline checkout not available, falling back to payment link');
        }

        if (useInlineCheckout && orderData) {
          // Open Razorpay Checkout popup
          const options = {
            key: orderData.key_id,
            amount: orderData.amount * 100, // in paise
            currency: "INR",
            name: "Retail Store",
            description: `Order ${orderRef.id.slice(-8).toUpperCase()}`,
            order_id: orderData.order_id,
            prefill: {
              name: customer.name,
              email: customer.email,
              contact: customer.phone || addressData.phone
            },
            notes: {
              order_id: orderRef.id,
              customer_id: customer.customer_id
            },
            theme: {
              color: "#3399cc"
            },
            handler: async function (response: { razorpay_payment_id: string; razorpay_order_id: string; razorpay_signature: string }) {
              // Payment successful - verify and update order
              try {
                const verifyResponse = await fetch(`${API_URL}/api/payment/verify?razorpay_order_id=${response.razorpay_order_id}&razorpay_payment_id=${response.razorpay_payment_id}&razorpay_signature=${response.razorpay_signature}`, {
                  method: 'POST',
                });
                
                // Update order status in Firestore
                const { doc, updateDoc } = await import('firebase/firestore');
                await updateDoc(doc(firestore, 'orders', orderRef.id), {
                  paymentStatus: 'paid',
                  razorpayPaymentId: response.razorpay_payment_id,
                  razorpayOrderId: response.razorpay_order_id,
                });
                
                toast({ title: "🎉 Payment Successful!", description: `You'll earn ${pointsToEarn} loyalty points!` });
                await clearCart();
                router.push(`/order-confirmation?order_id=${orderRef.id}&status=success`);
              } catch (err) {
                console.error("Payment verification error:", err);
                await clearCart();
                router.push(`/order-confirmation?order_id=${orderRef.id}&status=success`);
              }
            },
            modal: {
              ondismiss: function() {
                setIsProcessing(false);
                toast({ variant: "destructive", title: "Payment Cancelled", description: "You can retry the payment from your orders page." });
                // Redirect to order confirmation with failed status
                router.push(`/order-confirmation?order_id=${orderRef.id}&status=failed`);
              }
            }
          };

          const razorpay = new window.Razorpay(options);
          
          razorpay.on('payment.failed', function (response: any) {
            console.error("Payment failed:", response.error);
            setIsProcessing(false);
            toast({ 
              variant: "destructive", 
              title: "Payment Failed", 
              description: response.error.description || "Please try again."
            });
            router.push(`/order-confirmation?order_id=${orderRef.id}&status=failed`);
          });
          
          razorpay.open();
          return; // Don't set isProcessing to false here
        } else {
          // Fallback to payment link method
          const linkResponse = await fetch(`${API_URL}/api/payment/create-link`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              customer_id: customer.customer_id,
              amount: finalTotal,
              description: `Order with ${items.length} items`,
              items: items.map(item => ({
                sku: item.sku || item.productId,
                name: item.name,
                price: item.price,
                quantity: item.quantity
              }))
            }),
          });
          
          if (linkResponse.ok) {
            const paymentData = await linkResponse.json();
            if (paymentData.status === 'success' && paymentData.payment_url) {
              toast({ title: "Payment Link Created!", description: "Opening payment page..." });
              window.open(paymentData.payment_url, '_blank');
              await clearCart();
              router.push(`/order-confirmation?order_id=${orderRef.id}&status=success`);
              return;
            }
          }
          
          // If all payment methods fail, still allow the order but mark as pending
          toast({ title: "Order Placed!", description: "Please complete payment later." });
          await clearCart();
          router.push(`/order-confirmation?order_id=${orderRef.id}&status=pending`);
        }
      } else {
        // Cash on Delivery
        const orderRef = await addDoc(collection(firestore, 'orders'), {
          customerId: customer.customer_id,
          customerEmail: customer.email,
          customerName: customer.name,
          createdAt: serverTimestamp(),
          items: items,
          subtotal: totalPrice,
          loyaltyDiscount,
          couponDiscount,
          couponCode: appliedCoupon || null,
          shippingCost,
          total: finalTotal,
          pointsEarned: pointsToEarn,
          shippingAddress: addressData,
          paymentMethod: 'cod',
          paymentStatus: 'pending',
        });

        toast({ title: "🎉 Order Placed!", description: `You'll earn ${pointsToEarn} loyalty points!` });
        await clearCart();
        router.push(`/order-confirmation?order_id=${orderRef.id}&status=success`);
      }
    } catch (error: any) {
      console.error("Order Error:", error);
      toast({ variant: "destructive", title: "Order Failed", description: error.message || "There was a problem placing your order." });
    } finally {
      setIsProcessing(false);
    }
  };

  if (isCustomerLoading) {
    return <CheckoutSkeleton />;
  }

  if (!isAuthenticated) {
    return <CheckoutSkeleton />;
  }

  if (totalItems === 0 && !isProcessing) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold font-headline mb-4">Your Cart is Empty</h1>
        <p className="text-muted-foreground mb-6">Let's find something for you!</p>
        <Button asChild><Link href="/products">Start Shopping</Link></Button>
      </div>
    );
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'Platinum': return 'bg-gradient-to-r from-purple-500 to-pink-500 text-white';
      case 'Gold': return 'bg-gradient-to-r from-yellow-400 to-amber-500 text-white';
      case 'Silver': return 'bg-gradient-to-r from-gray-400 to-gray-500 text-white';
      default: return 'bg-gradient-to-r from-orange-400 to-orange-600 text-white';
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold font-headline mb-8">Checkout</h1>
      
      {/* Loyalty Status Banner */}
      {customer && (
        <Card className="mb-8 bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
          <CardContent className="py-4">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-full ${getTierColor(loyaltyTier)}`}>
                  <Crown className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-semibold">Welcome, {customer.name}!</p>
                  <div className="text-sm text-muted-foreground flex items-center gap-1">
                    <Badge className={getTierColor(loyaltyTier)}>{loyaltyTier}</Badge>
                    <span>• {customer.loyalty_points?.toLocaleString() || 0} Points</span>
                  </div>
                </div>
              </div>
              <div className="text-right">
                {loyaltyBenefit.discount > 0 && (
                  <p className="text-sm font-medium text-green-600">
                    🎁 {loyaltyBenefit.discount}% Loyalty Discount Applied!
                  </p>
                )}
                {loyaltyBenefit.freeShipping && (
                  <p className="text-sm font-medium text-green-600">
                    🚚 Free Shipping Unlocked!
                  </p>
                )}
                <p className="text-xs text-muted-foreground">
                  Earn {pointsToEarn} points on this order ({loyaltyBenefit.pointsMultiplier}x multiplier)
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid lg:grid-cols-2 gap-12">
        <div className="space-y-8">
          {/* Shipping Address Form */}
          <Card>
            <CardHeader>
              <CardTitle>Shipping Address</CardTitle>
              <CardDescription>Enter your delivery address</CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...addressForm}>
                <form className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <FormField control={addressForm.control} name="fullName" render={({ field }) => (
                      <FormItem>
                        <FormLabel>Full Name</FormLabel>
                        <FormControl><Input placeholder="Amit Verma" {...field} /></FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                    <FormField control={addressForm.control} name="phone" render={({ field }) => (
                      <FormItem>
                        <FormLabel>Phone</FormLabel>
                        <FormControl><Input placeholder="+91-9000000001" {...field} /></FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                  </div>
                  <FormField control={addressForm.control} name="address" render={({ field }) => (
                    <FormItem>
                      <FormLabel>Address</FormLabel>
                      <FormControl><Input placeholder="123, Main Street, Apartment 4B" {...field} /></FormControl>
                      <FormMessage />
                    </FormItem>
                  )} />
                  <div className="grid grid-cols-3 gap-4">
                    <FormField control={addressForm.control} name="city" render={({ field }) => (
                      <FormItem>
                        <FormLabel>City</FormLabel>
                        <FormControl><Input placeholder="Mumbai" {...field} /></FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                    <FormField control={addressForm.control} name="state" render={({ field }) => (
                      <FormItem>
                        <FormLabel>State</FormLabel>
                        <FormControl><Input placeholder="Maharashtra" {...field} /></FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                    <FormField control={addressForm.control} name="zipCode" render={({ field }) => (
                      <FormItem>
                        <FormLabel>PIN Code</FormLabel>
                        <FormControl><Input placeholder="400001" {...field} /></FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>

          {/* Payment Method */}
          <Card>
            <CardHeader>
              <CardTitle>Payment Method</CardTitle>
              <CardDescription>Choose how you'd like to pay</CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs value={paymentMethod} onValueChange={setPaymentMethod} className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="razorpay" className="gap-2">
                    <CreditCard className="h-4 w-4" />
                    Pay Online
                  </TabsTrigger>
                  <TabsTrigger value="cod" className="gap-2">
                    <Banknote className="h-4 w-4" />
                    Cash on Delivery
                  </TabsTrigger>
                </TabsList>
                <TabsContent value="razorpay" className="pt-4 text-center">
                  <p className="text-muted-foreground">Pay securely with Razorpay (Cards, UPI, Net Banking)</p>
                </TabsContent>
                <TabsContent value="cod" className="pt-4 text-center">
                  <p className="text-muted-foreground">Pay cash when your order is delivered</p>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <Button 
            onClick={addressForm.handleSubmit(handlePlaceOrder)} 
            className="w-full h-12 text-lg" 
            size="lg" 
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Processing...
              </>
            ) : (
              `Place Order - ₹${finalTotal.toLocaleString('en-IN')}`
            )}
          </Button>
        </div>

        <div className='space-y-8'>
          {/* Available Coupons */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Gift className="h-5 w-5 text-primary" />
                {isNewCustomer ? 'Welcome Offers!' : 'Available Offers'}
              </CardTitle>
              {isNewCustomer && (
                <CardDescription className="flex items-center gap-1">
                  <Sparkles className="h-4 w-4" />
                  Special discounts for new customers!
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-3">
              {availableCoupons.length > 0 ? (
                availableCoupons.map(([code, coupon]) => (
                  <div 
                    key={code} 
                    className={cn(
                      "flex items-center justify-between p-3 rounded-lg border transition-colors",
                      appliedCoupon === code 
                        ? "border-green-500 bg-green-500/10" 
                        : "border-dashed border-primary/50 bg-primary/5 hover:bg-primary/10"
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <TicketPercent className={cn("h-5 w-5", appliedCoupon === code ? "text-green-600" : "text-primary")} />
                      <div>
                        <p className="font-semibold text-sm">{code}</p>
                        <p className="text-xs text-muted-foreground">{coupon.description}</p>
                        {coupon.minOrder > 0 && (
                          <p className="text-xs text-muted-foreground">Min. order: ₹{coupon.minOrder}</p>
                        )}
                      </div>
                    </div>
                    {appliedCoupon === code ? (
                      <Button variant="ghost" size="sm" onClick={removeCoupon} className="text-red-500 hover:text-red-600">
                        Remove
                      </Button>
                    ) : (
                      <Button variant="outline" size="sm" onClick={() => applyCoupon(code)}>
                        Apply
                      </Button>
                    )}
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No coupons available for your current order
                </p>
              )}
            </CardContent>
          </Card>

          {/* Order Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-64 overflow-y-auto">
                {items.map(item => (
                  <div key={item.id} className="flex items-center gap-4">
                    <div className="relative h-16 w-16 rounded-md overflow-hidden border bg-muted flex-shrink-0">
                      {item.image && <Image src={item.image} alt={item.name} fill className="object-contain p-1" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">{item.name}</p>
                      <p className="text-xs text-muted-foreground">Qty: {item.quantity}</p>
                    </div>
                    <p className="font-medium text-sm">₹{(item.price * item.quantity).toLocaleString('en-IN')}</p>
                  </div>
                ))}
              </div>
              
              <Separator className="my-4" />
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Subtotal ({totalItems} items)</span>
                  <span>₹{totalPrice.toLocaleString('en-IN')}</span>
                </div>
                
                {loyaltyDiscount > 0 && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span className="flex items-center gap-1">
                      <Crown className="h-3 w-3" />
                      {loyaltyTier} Discount ({loyaltyBenefit.discount}%)
                    </span>
                    <span>- ₹{loyaltyDiscount.toLocaleString('en-IN')}</span>
                  </div>
                )}
                
                {couponDiscount > 0 && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span className="flex items-center gap-1">
                      <TicketPercent className="h-3 w-3" />
                      Coupon ({appliedCoupon})
                    </span>
                    <span>- ₹{couponDiscount.toLocaleString('en-IN')}</span>
                  </div>
                )}
                
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground flex items-center gap-1">
                    Shipping
                    {loyaltyBenefit.freeShipping && <Badge variant="secondary" className="text-xs">FREE</Badge>}
                  </span>
                  <span className={loyaltyBenefit.freeShipping ? "line-through text-muted-foreground" : ""}>
                    ₹{baseShippingCost}
                  </span>
                </div>
                
                <Separator className="my-2" />
                
                <div className="flex justify-between font-bold text-lg">
                  <span>Total</span>
                  <span>₹{finalTotal.toLocaleString('en-IN')}</span>
                </div>
                
                {(loyaltyDiscount > 0 || couponDiscount > 0 || loyaltyBenefit.freeShipping) && (
                  <div className="text-center pt-2">
                    <Badge variant="secondary" className="bg-green-100 text-green-700">
                      🎉 You're saving ₹{(loyaltyDiscount + couponDiscount + (loyaltyBenefit.freeShipping ? baseShippingCost : 0)).toLocaleString('en-IN')}!
                    </Badge>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
