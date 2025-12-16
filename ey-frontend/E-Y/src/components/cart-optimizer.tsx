'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { useCart } from '@/hooks/use-cart';
import { useCustomer } from '@/context/customer-context';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Sparkles, 
  Truck, 
  Gift, 
  Tag, 
  TrendingDown, 
  ShoppingBag,
  ChevronDown,
  ChevronUp,
  Check,
  Copy,
  Zap
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Suggestion {
  id: string;
  type: 'free_shipping' | 'loyalty_points' | 'promo_code' | 'bundle' | 'savings';
  icon: React.ReactNode;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  savings?: number;
  priority: number;
}

// Available promo codes
const PROMO_CODES = [
  { code: 'WELCOME10', discount: 10, type: 'percent', minPurchase: 500, description: '10% off on orders above ₹500' },
  { code: 'FLAT200', discount: 200, type: 'flat', minPurchase: 2000, description: '₹200 off on orders above ₹2000' },
  { code: 'SAVE500', discount: 500, type: 'flat', minPurchase: 5000, description: '₹500 off on orders above ₹5000' },
  { code: 'MEGA1000', discount: 1000, type: 'flat', minPurchase: 10000, description: '₹1000 off on orders above ₹10,000' },
  { code: 'FREESHIP', discount: 0, type: 'shipping', minPurchase: 999, description: 'Free shipping on orders above ₹999' },
];

const FREE_SHIPPING_THRESHOLD = 999;

export function CartOptimizer() {
  const { items, totalPrice, totalItems } = useCart();
  const { customer, isAuthenticated } = useCustomer();
  const { toast } = useToast();
  const [isExpanded, setIsExpanded] = useState(true);
  const [appliedPromo, setAppliedPromo] = useState<string | null>(null);

  // Calculate loyalty points value (10 points = ₹1)
  const loyaltyPointsValue = customer?.loyalty_points ? Math.floor(customer.loyalty_points / 10) : 0;
  const canUseLoyaltyPoints = loyaltyPointsValue >= 10 && isAuthenticated;

  // Find best applicable promo code
  const bestPromoCode = useMemo(() => {
    const applicable = PROMO_CODES.filter(promo => totalPrice >= promo.minPurchase);
    if (applicable.length === 0) return null;
    
    // Calculate actual savings for each
    const withSavings = applicable.map(promo => {
      let savings = 0;
      if (promo.type === 'percent') {
        savings = (totalPrice * promo.discount) / 100;
      } else if (promo.type === 'flat') {
        savings = promo.discount;
      } else if (promo.type === 'shipping') {
        savings = 99; // Assumed shipping cost
      }
      return { ...promo, savings };
    });
    
    // Return highest savings
    return withSavings.sort((a, b) => b.savings - a.savings)[0];
  }, [totalPrice]);

  // Find next tier promo code
  const nextPromoCode = useMemo(() => {
    const notApplicable = PROMO_CODES.filter(promo => totalPrice < promo.minPurchase);
    if (notApplicable.length === 0) return null;
    return notApplicable.sort((a, b) => a.minPurchase - b.minPurchase)[0];
  }, [totalPrice]);

  // Generate suggestions
  const suggestions = useMemo(() => {
    const result: Suggestion[] = [];

    // 1. Free shipping suggestion
    if (totalPrice < FREE_SHIPPING_THRESHOLD) {
      const amountNeeded = FREE_SHIPPING_THRESHOLD - totalPrice;
      result.push({
        id: 'free-shipping',
        type: 'free_shipping',
        icon: <Truck className="h-5 w-5 text-blue-500" />,
        title: `Add ₹${amountNeeded.toFixed(0)} more for FREE shipping!`,
        description: `Orders above ₹${FREE_SHIPPING_THRESHOLD} qualify for free delivery`,
        action: {
          label: 'Browse Products',
          onClick: () => window.location.href = '/products',
        },
        savings: 99,
        priority: 1,
      });
    } else {
      result.push({
        id: 'free-shipping-qualified',
        type: 'free_shipping',
        icon: <Truck className="h-5 w-5 text-green-500" />,
        title: '🎉 You qualify for FREE shipping!',
        description: 'Your order will be delivered for free',
        savings: 99,
        priority: 5,
      });
    }

    // 2. Loyalty points suggestion
    if (canUseLoyaltyPoints) {
      result.push({
        id: 'loyalty-points',
        type: 'loyalty_points',
        icon: <Gift className="h-5 w-5 text-pink-500" />,
        title: `Use ${customer?.loyalty_points} points for ₹${loyaltyPointsValue} off!`,
        description: `You have ${customer?.loyalty_points} loyalty points (${customer?.loyalty_tier} member)`,
        action: {
          label: 'Apply Points',
          onClick: () => {
            toast({
              title: '✨ Points Applied!',
              description: `₹${loyaltyPointsValue} discount will be applied at checkout`,
            });
          },
        },
        savings: loyaltyPointsValue,
        priority: 2,
      });
    } else if (isAuthenticated && customer) {
      result.push({
        id: 'loyalty-earn',
        type: 'loyalty_points',
        icon: <Gift className="h-5 w-5 text-pink-500" />,
        title: `Earn ${Math.floor(totalPrice / 10)} points on this order!`,
        description: `${customer.loyalty_tier} members earn 1 point per ₹10 spent`,
        priority: 4,
      });
    }

    // 3. Best promo code suggestion
    if (bestPromoCode && !appliedPromo) {
      result.push({
        id: 'best-promo',
        type: 'promo_code',
        icon: <Tag className="h-5 w-5 text-orange-500" />,
        title: `Apply code "${bestPromoCode.code}" to save ₹${bestPromoCode.savings?.toFixed(0)}!`,
        description: bestPromoCode.description,
        action: {
          label: 'Copy Code',
          onClick: () => {
            navigator.clipboard.writeText(bestPromoCode.code);
            setAppliedPromo(bestPromoCode.code);
            toast({
              title: '📋 Code Copied!',
              description: `Use "${bestPromoCode.code}" at checkout`,
            });
          },
        },
        savings: bestPromoCode.savings,
        priority: 1,
      });
    }

    // 4. Next tier promo suggestion
    if (nextPromoCode && !bestPromoCode) {
      const amountNeeded = nextPromoCode.minPurchase - totalPrice;
      result.push({
        id: 'next-promo',
        type: 'promo_code',
        icon: <TrendingDown className="h-5 w-5 text-purple-500" />,
        title: `Add ₹${amountNeeded.toFixed(0)} more to unlock "${nextPromoCode.code}"!`,
        description: nextPromoCode.description,
        action: {
          label: 'Shop More',
          onClick: () => window.location.href = '/products',
        },
        priority: 3,
      });
    }

    // 5. Bundle/combo suggestion based on cart items
    if (totalItems >= 2) {
      const potentialSavings = Math.floor(totalPrice * 0.05); // 5% bundle discount
      if (potentialSavings >= 50) {
        result.push({
          id: 'bundle-savings',
          type: 'bundle',
          icon: <ShoppingBag className="h-5 w-5 text-indigo-500" />,
          title: 'Multi-item discount available!',
          description: `You could save up to ₹${potentialSavings} with our bundle offers`,
          action: {
            label: 'View Bundles',
            onClick: () => {
              toast({
                title: '🎁 Bundle Deals',
                description: 'Ask our AI assistant about combo offers!',
              });
            },
          },
          savings: potentialSavings,
          priority: 4,
        });
      }
    }

    // Sort by priority
    return result.sort((a, b) => a.priority - b.priority);
  }, [totalPrice, totalItems, customer, isAuthenticated, canUseLoyaltyPoints, loyaltyPointsValue, bestPromoCode, nextPromoCode, appliedPromo, toast]);

  // Calculate total potential savings
  const totalSavings = useMemo(() => {
    return suggestions.reduce((sum, s) => sum + (s.savings || 0), 0);
  }, [suggestions]);

  if (totalItems === 0) return null;

  return (
    <Card className="border-primary/20 bg-gradient-to-br from-primary/5 to-transparent">
      <CardHeader 
        className="cursor-pointer py-3"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-primary/10 rounded-full">
              <Zap className="h-4 w-4 text-primary" />
            </div>
            <CardTitle className="text-base font-semibold">Smart Savings</CardTitle>
            {totalSavings > 0 && (
              <Badge variant="secondary" className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                Save up to ₹{totalSavings}
              </Badge>
            )}
          </div>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
        </div>
      </CardHeader>
      
      {isExpanded && (
        <CardContent className="pt-0 space-y-3">
          {suggestions.slice(0, 4).map((suggestion) => (
            <div
              key={suggestion.id}
              className="flex items-start gap-3 p-3 rounded-lg bg-background/50 border border-border/50 hover:border-primary/30 transition-colors"
            >
              <div className="flex-shrink-0 mt-0.5">
                {suggestion.icon}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium leading-tight">{suggestion.title}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{suggestion.description}</p>
              </div>
              {suggestion.action && (
                <Button 
                  size="sm" 
                  variant="outline"
                  className="flex-shrink-0 h-7 text-xs"
                  onClick={(e) => {
                    e.stopPropagation();
                    suggestion.action?.onClick();
                  }}
                >
                  {appliedPromo === (suggestion as any).code ? (
                    <>
                      <Check className="h-3 w-3 mr-1" />
                      Applied
                    </>
                  ) : (
                    suggestion.action.label
                  )}
                </Button>
              )}
            </div>
          ))}
          
          {/* Summary footer */}
          <div className="pt-2 border-t border-border/50">
            <p className="text-xs text-muted-foreground flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              <span>AI-powered suggestions to maximize your savings</span>
            </p>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
