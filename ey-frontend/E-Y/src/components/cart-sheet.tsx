

'use client';

import { useCart } from '@/hooks/use-cart';
import { useCustomer } from '@/context/customer-context';
import { Button } from '@/components/ui/button';
import Image from 'next/image';
import Link from 'next/link';
import { ScrollArea } from './ui/scroll-area';
import { SheetFooter, SheetClose } from './ui/sheet';
import { Trash2, Truck, Gift, Zap } from 'lucide-react';

const FREE_SHIPPING_THRESHOLD = 999;

export function CartSheet() {
  const { items, removeItem, updateQuantity, totalItems, totalPrice } = useCart();
  const { customer, isAuthenticated } = useCustomer();
  
  const amountForFreeShipping = FREE_SHIPPING_THRESHOLD - totalPrice;
  const qualifiesForFreeShipping = totalPrice >= FREE_SHIPPING_THRESHOLD;
  const loyaltyPointsValue = customer?.loyalty_points ? Math.floor(customer.loyalty_points / 10) : 0;

  return (
    <div className="h-full flex flex-col">
      {totalItems > 0 ? (
        <>
          <ScrollArea className="flex-grow pr-4 -mr-6">
            <div className="divide-y">
              {items.map((item) => {
                const productImage = item.image;
                return (
                  <div key={item.id} className="flex items-center py-4">
                    <div className="relative h-24 w-20 flex-shrink-0 overflow-hidden rounded-md">
                      {productImage ? (
                        <Image
                          src={productImage}
                          alt={item.name}
                          fill
                          className="object-cover"
                        />
                      ) : (
                        <div className="bg-muted w-full h-full" />
                      )}
                    </div>
                    <div className="ml-4 flex-1">
                      <h4 className="font-medium text-sm">
                        <Link href={`/shops/products/${item.productId}`} className="hover:underline">
                          {item.name}
                        </Link>
                      </h4>
                      <p className="text-xs text-muted-foreground">Size: {item.size}</p>
                      <p className="text-sm font-semibold mt-1">₹{item.price.toFixed(2)}</p>
                      <div className="flex items-center justify-between mt-2">
                        <div className="flex items-center border rounded-md">
                          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => updateQuantity(item.id, item.quantity - 1)} disabled={item.quantity <= 1}>
                            -
                          </Button>
                          <span className="w-8 text-center text-sm">{item.quantity}</span>
                          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => updateQuantity(item.id, item.quantity + 1)}>
                            +
                          </Button>
                        </div>
                        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive" onClick={() => removeItem(item.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>
          
          {/* Smart Savings Mini Section */}
          <div className="border-t pt-3 pb-2 space-y-2">
            <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
              <Zap className="h-3 w-3 text-primary" />
              <span>Smart Savings</span>
            </div>
            
            {!qualifiesForFreeShipping ? (
              <div className="flex items-center gap-2 text-xs bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 p-2 rounded-md">
                <Truck className="h-3.5 w-3.5 flex-shrink-0" />
                <span>Add ₹{amountForFreeShipping.toFixed(0)} more for FREE shipping!</span>
              </div>
            ) : (
              <div className="flex items-center gap-2 text-xs bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 p-2 rounded-md">
                <Truck className="h-3.5 w-3.5 flex-shrink-0" />
                <span>🎉 You get FREE shipping!</span>
              </div>
            )}
            
            {isAuthenticated && loyaltyPointsValue >= 10 && (
              <div className="flex items-center gap-2 text-xs bg-pink-50 dark:bg-pink-900/20 text-pink-700 dark:text-pink-300 p-2 rounded-md">
                <Gift className="h-3.5 w-3.5 flex-shrink-0" />
                <span>Use {customer?.loyalty_points} points for ₹{loyaltyPointsValue} off!</span>
              </div>
            )}
          </div>
          
          <SheetFooter className="mt-auto border-t pt-4">
            <div className="w-full space-y-4">
              <div className="flex justify-between font-semibold">
                <span>Subtotal</span>
                <span>₹{totalPrice.toFixed(2)}</span>
              </div>
              <SheetClose asChild>
                <Button asChild className="w-full">
                  <Link href="/cart">View Cart & Checkout</Link>
                </Button>
              </SheetClose>
            </div>
          </SheetFooter>
        </>
      ) : (
        <div className="flex h-full flex-col items-center justify-center text-center">
          <h3 className="text-lg font-semibold">Your cart is empty</h3>
          <p className="text-sm text-muted-foreground mt-2">Add items to see them here.</p>
          <SheetClose asChild>
            <Button asChild className="mt-4">
              <Link href="/products">Start Shopping</Link>
            </Button>
          </SheetClose>
        </div>
      )}
    </div>
  );
}
