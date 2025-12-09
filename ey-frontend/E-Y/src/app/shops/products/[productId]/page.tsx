

'use client';

import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import type { Product } from '@/lib/types';
import { useCart } from '@/hooks/use-cart';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';
import Link from 'next/link';
import { Star, ShoppingCart, Truck, Shield, RotateCcw, Check, Minus, Plus, Package, MapPin } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function StarRating({ rating, size = 'md' }: { rating: number, size?: 'sm' | 'md' | 'lg' }) {
    const starSize = { sm: 'h-4 w-4', md: 'h-5 w-5', lg: 'h-6 w-6' }[size];
    return (
        <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
                <Star key={i} className={`${starSize} ${i < Math.round(rating) ? 'text-yellow-400 fill-yellow-400' : 'text-muted-foreground/30'}`} />
            ))}
        </div>
    );
}

function ProductPageSkeleton() {
    return (
      <div className="grid md:grid-cols-2 gap-8 lg:gap-16">
        <div className="space-y-4">
            <Skeleton className="aspect-square w-full rounded-lg" />
            <div className="grid grid-cols-5 gap-4">
                {Array.from({ length: 4 }).map((_, i) => (
                    <Skeleton key={i} className="aspect-square rounded-md" />
                ))}
            </div>
        </div>
        <div className="space-y-6">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-6 w-1/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-12 w-full" />
        </div>
      </div>
    );
}

type InventoryItem = {
  location: string;
  quantity: number;
};

export default function ProductPage() {
    const params = useParams();
    const productId = params.productId as string;
    const { toast } = useToast();
    const { addItem } = useCart();
    
    const [product, setProduct] = useState<Product | null>(null);
    const [inventory, setInventory] = useState<InventoryItem[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [mainImage, setMainImage] = useState<string | null>(null);
    const [quantity, setQuantity] = useState(1);
    const [isAdding, setIsAdding] = useState(false);
    const [justAdded, setJustAdded] = useState(false);

    useEffect(() => {
      async function fetchProduct() {
        try {
          setIsLoading(true);
          const response = await fetch(`${API_URL}/api/products/${productId}`);
          if (!response.ok) throw new Error('Product not found');
          const data = await response.json();
          setProduct(data);
          setInventory(data.inventory || []);
          if (data.images?.length > 0) {
            setMainImage(data.images[0]);
          }
        } catch (err) {
          console.error('Error fetching product:', err);
          setProduct(null);
        } finally {
          setIsLoading(false);
        }
      }
      if (productId) {
        fetchProduct();
      }
    }, [productId]);
  
    const handleAddToCart = async () => {
      if (!product) return;
      
      setIsAdding(true);
      try {
        addItem(product, undefined, quantity);
        setJustAdded(true);
        toast({
          title: 'Added to Cart! 🛒',
          description: `${quantity}x ${product.name} has been added to your cart.`,
        });
        setTimeout(() => setJustAdded(false), 2000);
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Could not add item to cart. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setIsAdding(false);
      }
    };

    if (isLoading) {
      return (
        <div className="container mx-auto px-4 py-8">
          <ProductPageSkeleton />
        </div>
      );
    }
  
    if (!product) {
      return (
        <div className="container mx-auto px-4 py-8 text-center py-20">
          <h1 className="text-2xl font-bold">Product Not Found</h1>
          <p className="text-muted-foreground mt-2">Sorry, we couldn't find the product you're looking for.</p>
          <Button asChild className="mt-6">
            <Link href="/products">Browse Products</Link>
          </Button>
        </div>
      );
    }
  
    const firstImage = mainImage ?? (product.images?.length > 0 ? product.images[0] : null);
    const isOnSale = typeof product.originalPrice === 'number' && product.originalPrice > product.price;
    const discountPercent = isOnSale && product.originalPrice 
      ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
      : 0;
    const isSoldOut = product.stock === 0 || product.inStock === false;
    const totalStock = inventory.reduce((sum, inv) => sum + inv.quantity, 0) || product.stock || 0;

    return (
      <div className="container mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <Breadcrumb className="mb-8">
          <BreadcrumbList>
            <BreadcrumbItem><Link href="/">Home</Link></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><Link href="/products">Products</Link></BreadcrumbItem>
            {product.category && (
              <>
                <BreadcrumbSeparator />
                <BreadcrumbItem><Link href={`/products?category=${product.category}`}>{product.category}</Link></BreadcrumbItem>
              </>
            )}
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>{product.name}</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <div className="grid md:grid-cols-2 gap-8 lg:gap-16">
          {/* Image Gallery */}
          <div>
            <div className="aspect-square w-full overflow-hidden rounded-lg mb-4 border bg-muted relative">
              {isOnSale && (
                <Badge variant="destructive" className="absolute top-4 left-4 z-10 text-sm">
                  -{discountPercent}% OFF
                </Badge>
              )}
              {firstImage ? (
                <Image
                  src={firstImage}
                  alt={product.name}
                  width={600}
                  height={600}
                  className="object-contain w-full h-full p-4"
                  priority
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <span className="text-muted-foreground">{product.category}</span>
                </div>
              )}
              {isSoldOut && (
                <div className="absolute inset-0 bg-background/80 flex items-center justify-center">
                  <span className="text-2xl font-bold text-destructive">SOLD OUT</span>
                </div>
              )}
            </div>
            {product.images && product.images.length > 1 && (
              <div className="grid grid-cols-5 gap-2">
                {product.images.map((imgSrc, index) => (
                  <button
                    key={index}
                    onClick={() => setMainImage(imgSrc)}
                    className={cn(
                      "aspect-square overflow-hidden rounded-md border-2 bg-muted",
                      mainImage === imgSrc ? 'border-primary' : 'border-transparent hover:border-muted-foreground/50'
                    )}
                  >
                    <Image
                      src={imgSrc}
                      alt={`${product.name} thumbnail ${index + 1}`}
                      width={100}
                      height={100}
                      className="object-contain w-full h-full p-1"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>
  
          {/* Product Details */}
          <div className="flex flex-col">
            {/* Category & Brand */}
            <div className="flex items-center gap-2 mb-2">
              {product.category && <Badge variant="secondary">{product.category}</Badge>}
              {product.brand && <span className="text-sm text-muted-foreground">by {product.brand}</span>}
            </div>

            {/* Title */}
            <h1 className="text-3xl font-bold font-headline">{product.name}</h1>
            
            {/* SKU */}
            {product.sku && (
              <p className="text-sm text-muted-foreground mt-1">SKU: {product.sku}</p>
            )}

            {/* Rating */}
            {product.rating && (
              <div className="mt-3 flex items-center gap-2">
                <StarRating rating={product.rating} />
                <span className="text-muted-foreground text-sm">
                  ({product.rating.toFixed(1)} from {product.reviewCount || 0} reviews)
                </span>
              </div>
            )}

            {/* Price */}
            <div className="mt-4 flex items-baseline gap-3">
              <span className={cn("text-3xl font-bold", isOnSale && "text-destructive")}>
                ₹{product.price.toLocaleString('en-IN')}
              </span>
              {isOnSale && product.originalPrice && (
                <span className="text-xl text-muted-foreground line-through">
                  ₹{product.originalPrice.toLocaleString('en-IN')}
                </span>
              )}
              {isOnSale && (
                <Badge variant="destructive">Save ₹{(product.originalPrice! - product.price).toLocaleString('en-IN')}</Badge>
              )}
            </div>

            <Separator className="my-6" />

            {/* Description */}
            <p className="text-muted-foreground leading-relaxed">{product.description}</p>

            {/* Stock Status */}
            <div className="mt-6 flex items-center gap-2">
              <Package className="h-5 w-5 text-muted-foreground" />
              {isSoldOut ? (
                <span className="text-destructive font-medium">Out of Stock</span>
              ) : totalStock < 10 ? (
                <span className="text-orange-500 font-medium">Only {totalStock} left in stock!</span>
              ) : (
                <span className="text-green-600 font-medium">In Stock ({totalStock} available)</span>
              )}
            </div>

            {/* Quantity Selector */}
            {!isSoldOut && (
              <div className="mt-6">
                <label className="text-sm font-medium mb-2 block">Quantity</label>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => setQuantity(q => Math.max(1, q - 1))}
                    disabled={quantity <= 1}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <span className="w-12 text-center font-medium text-lg">{quantity}</span>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => setQuantity(q => Math.min(totalStock, q + 1))}
                    disabled={quantity >= totalStock}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}

            {/* Add to Cart Button */}
            <Button 
              onClick={handleAddToCart} 
              size="lg" 
              className={cn("w-full mt-6", justAdded && "bg-green-600 hover:bg-green-700")}
              disabled={isSoldOut || isAdding}
            >
              {justAdded ? (
                <>
                  <Check className="mr-2 h-5 w-5" />
                  Added to Cart!
                </>
              ) : (
                <>
                  <ShoppingCart className="mr-2 h-5 w-5" />
                  Add to Cart - ₹{(product.price * quantity).toLocaleString('en-IN')}
                </>
              )}
            </Button>

            {/* Trust Badges */}
            <div className="mt-8 grid grid-cols-3 gap-4">
              <div className="flex flex-col items-center text-center p-3 border rounded-lg">
                <Truck className="h-6 w-6 text-primary mb-2" />
                <span className="text-xs font-medium">Free Shipping</span>
                <span className="text-xs text-muted-foreground">On orders over ₹999</span>
              </div>
              <div className="flex flex-col items-center text-center p-3 border rounded-lg">
                <Shield className="h-6 w-6 text-primary mb-2" />
                <span className="text-xs font-medium">1 Year Warranty</span>
                <span className="text-xs text-muted-foreground">Manufacturer warranty</span>
              </div>
              <div className="flex flex-col items-center text-center p-3 border rounded-lg">
                <RotateCcw className="h-6 w-6 text-primary mb-2" />
                <span className="text-xs font-medium">Easy Returns</span>
                <span className="text-xs text-muted-foreground">7-day return policy</span>
              </div>
            </div>
          </div>
        </div>

        {/* Inventory Locations */}
        {inventory.length > 0 && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="h-5 w-5" />
                Available at Warehouses
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {inventory.map((inv, idx) => (
                  <div key={idx} className="flex justify-between items-center p-3 border rounded-lg">
                    <span className="font-medium">{inv.location}</span>
                    <Badge variant={inv.quantity > 50 ? "default" : inv.quantity > 0 ? "secondary" : "destructive"}>
                      {inv.quantity} units
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* AI Assistant CTA */}
        <Card className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardContent className="p-6 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-lg">Need help deciding?</h3>
              <p className="text-muted-foreground">Our AI assistant can help you find the perfect product</p>
            </div>
            <Button asChild>
              <Link href="/chatbot">
                Chat with AI Assistant
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
}