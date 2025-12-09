'use client';

import Link from 'next/link';
import Image from 'next/image';
import type { Product } from '@/lib/types';
import { Button } from './ui/button';
import { Plus, Star, ShoppingCart, Eye, Check } from 'lucide-react';
import { Badge } from './ui/badge';
import { useCart } from '@/hooks/use-cart';
import { useToast } from '@/hooks/use-toast';
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface ProductCardProps {
  product: Product;
  viewMode?: 'grid' | 'list';
}

export function ProductCard({ product, viewMode = 'grid' }: ProductCardProps) {
  const { addItem } = useCart();
  const { toast } = useToast();
  const [isAdding, setIsAdding] = useState(false);
  const [justAdded, setJustAdded] = useState(false);

  const firstImage = product.images?.[0];
  const isOnSale = typeof product.originalPrice === 'number' && product.originalPrice > product.price;
  const isSoldOut = product.stock === 0 || product.inStock === false;
  const discountPercent = isOnSale && product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0;

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (isSoldOut) return;
    
    setIsAdding(true);
    
    try {
      addItem(product, 'M', 1);
      
      setJustAdded(true);
      toast({
        title: "Added to Cart! 🛒",
        description: `${product.name} has been added to your cart.`,
      });
      
      setTimeout(() => setJustAdded(false), 2000);
    } catch (error) {
      toast({
        title: "Error",
        description: "Could not add item to cart. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsAdding(false);
    }
  };

  if (viewMode === 'list') {
    return (
      <div className="group flex gap-4 p-4 border rounded-lg hover:shadow-md transition-shadow bg-card">
        <Link href={`/shops/products/${product.id}`} className="relative w-32 h-32 flex-shrink-0">
          <div className="relative w-full h-full rounded-md overflow-hidden bg-muted">
            {firstImage ? (
              <Image src={firstImage} alt={product.name} fill className="object-contain p-2" sizes="128px" />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <span className="text-xs text-muted-foreground">{product.category}</span>
              </div>
            )}
            {isSoldOut && (
              <div className="absolute inset-0 bg-background/70 flex items-center justify-center">
                <span className="text-destructive font-bold text-sm">SOLD OUT</span>
              </div>
            )}
          </div>
        </Link>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {product.category && <Badge variant="secondary" className="text-xs">{product.category}</Badge>}
                {isOnSale && <Badge variant="destructive" className="text-xs">-{discountPercent}%</Badge>}
              </div>
              <Link href={`/shops/products/${product.id}`}>
                <h3 className="font-medium text-foreground hover:text-primary transition-colors line-clamp-1">{product.name}</h3>
              </Link>
              {product.brand && <p className="text-sm text-muted-foreground">{product.brand}</p>}
              <p className="text-sm text-muted-foreground line-clamp-2 mt-1">{product.description}</p>
              <div className="flex items-center gap-4 mt-2">
                {product.rating && (
                  <div className="flex items-center gap-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm font-medium">{product.rating.toFixed(1)}</span>
                  </div>
                )}
                {product.sku && <span className="text-xs text-muted-foreground">SKU: {product.sku}</span>}
              </div>
            </div>
            <div className="flex flex-col items-end gap-2">
              <div className="text-right">
                <p className={cn("text-lg font-bold", isOnSale && "text-destructive")}>₹{product.price.toLocaleString('en-IN')}</p>
                {isOnSale && product.originalPrice && (
                  <p className="text-sm text-muted-foreground line-through">₹{product.originalPrice.toLocaleString('en-IN')}</p>
                )}
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" asChild>
                  <Link href={`/shops/products/${product.id}`}><Eye className="h-4 w-4 mr-1" />View</Link>
                </Button>
                <Button size="sm" onClick={handleAddToCart} disabled={isSoldOut || isAdding} className={cn(justAdded && "bg-green-600 hover:bg-green-700")}>
                  {justAdded ? <><Check className="h-4 w-4 mr-1" />Added</> : <><ShoppingCart className="h-4 w-4 mr-1" />Add</>}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="group relative">
      <Link href={`/shops/products/${product.id}`}>
        <div className="overflow-hidden rounded-lg">
          <div className="relative aspect-square bg-muted">
            <div className="absolute top-2 left-2 z-10 flex flex-col gap-1">
              {!isSoldOut && isOnSale && <Badge variant="destructive">-{discountPercent}%</Badge>}
            </div>
            {product.category && (
              <Badge variant="secondary" className="absolute top-2 right-2 z-10 text-xs">{product.category}</Badge>
            )}
            {firstImage ? (
              <Image src={firstImage} alt={product.name} fill className="object-contain p-2 transition-transform duration-300 group-hover:scale-105" sizes="(max-width: 768px) 50vw, (max-width: 1200px) 25vw, 20vw" />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
                <span className="text-sm text-muted-foreground">{product.category || 'Product'}</span>
              </div>
            )}
            {isSoldOut && (
              <div className="absolute inset-0 bg-background/70 z-10 flex items-center justify-center">
                <span className="text-destructive-foreground font-bold text-xl tracking-widest">SOLD OUT</span>
              </div>
            )}
            {!isSoldOut && (
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors z-5 flex items-center justify-center opacity-0 group-hover:opacity-100">
                <Button size="sm" className={cn("transform translate-y-4 group-hover:translate-y-0 transition-all", justAdded && "bg-green-600 hover:bg-green-700")} onClick={handleAddToCart} disabled={isAdding}>
                  {justAdded ? <><Check className="h-4 w-4 mr-1" />Added!</> : <><ShoppingCart className="h-4 w-4 mr-1" />Quick Add</>}
                </Button>
              </div>
            )}
          </div>
        </div>
      </Link>
      <div className="mt-4 flex justify-between">
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-sm text-foreground truncate">
            <Link href={`/shops/products/${product.id}`} className="hover:text-primary transition-colors">{product.name}</Link>
          </h3>
          {product.brand && <p className="text-xs text-muted-foreground truncate">{product.brand}</p>}
          {product.rating && (
            <div className="flex items-center gap-1 mt-1">
              <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
              <span className="text-xs text-muted-foreground">{product.rating.toFixed(1)}</span>
            </div>
          )}
          <div className="flex items-baseline gap-2 mt-1">
            <p className={cn("font-semibold", isOnSale ? "text-destructive" : "text-foreground")}>₹{product.price.toLocaleString('en-IN')}</p>
            {isOnSale && product.originalPrice && (
              <p className="font-semibold text-sm text-muted-foreground line-through">₹{product.originalPrice.toLocaleString('en-IN')}</p>
            )}
          </div>
        </div>
        <Button variant="outline" size="icon" className={cn("shrink-0 transition-colors", justAdded && "bg-green-100 border-green-500 text-green-600")} disabled={isSoldOut || isAdding} onClick={handleAddToCart}>
          {justAdded ? <Check className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
        </Button>
      </div>
    </div>
  );
}
