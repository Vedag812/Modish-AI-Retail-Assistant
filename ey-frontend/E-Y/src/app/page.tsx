
'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Link from 'next/link';
import { ProductCard } from '@/components/product-card';
import { useEffect, useState } from 'react';
import type { Product } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { Shirt, ShoppingBag, Sparkles, MessageCircle, TrendingUp, Truck, Shield, Gift, ArrowRight, Monitor, MapPin, Smartphone, Store, Mic } from 'lucide-react';
import Image from 'next/image';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Fashion category data with images
const fashionCategories = [
  { 
    name: "Men's Fashion", 
    slug: 'Clothing - Men',
    href: '/shops/men',
    image: '👔',
    description: 'Kurtas, Shirts, Jeans & More',
    color: 'from-blue-500 to-indigo-600'
  },
  { 
    name: "Women's Fashion", 
    slug: 'Clothing - Women',
    href: '/shops/women',
    image: '👗',
    description: 'Sarees, Kurtis, Dresses & More',
    color: 'from-pink-500 to-rose-600'
  },
  { 
    name: 'Footwear', 
    slug: 'Footwear',
    href: '/products?category=Footwear',
    image: '👟',
    description: 'Shoes, Sandals, Heels & More',
    color: 'from-amber-500 to-orange-600'
  },
];

// Features/USPs
const features = [
  { icon: Truck, title: 'Free Shipping', description: 'On orders above ₹500' },
  { icon: Shield, title: 'Easy Returns', description: '7-day return policy' },
  { icon: Gift, title: 'Loyalty Rewards', description: 'Earn points on every purchase' },
  { icon: Mic, title: 'Voice Shopping', description: 'Talk to our AI assistant' },
];

function ProductsSkeleton() {
  return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
               <div key={i} className="space-y-3">
                  <Skeleton className="aspect-[3/4] rounded-lg" />
                  <Skeleton className="h-4 w-2/3" />
                  <Skeleton className="h-4 w-1/3" />
              </div>
          ))}
      </div>
  )
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch(`${API_URL}/api/products?limit=8`);
        if (!response.ok) throw new Error('Failed to fetch products');
        const data = await response.json();
        setProducts(data.products || []);
        
        // Get total count
        const countResponse = await fetch(`${API_URL}/api/products?limit=500`);
        if (countResponse.ok) {
          const countData = await countResponse.json();
          setTotalCount(countData.count || countData.products?.length || 0);
        }
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Could not load products. Make sure the API server is running.');
      } finally {
        setIsLoading(false);
      }
    }
    fetchProducts();
  }, []);

  return (
    <div className="space-y-16 -mt-8">
      {/* Hero Section */}
      <section className="relative h-[70vh] min-h-[500px] w-full -mx-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-pink-500 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-blue-500 rounded-full blur-3xl" />
        </div>
        <div className="relative h-full flex flex-col items-center justify-center text-center text-white p-4">
          <span className="px-4 py-1.5 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/20">
            ✨ New Winter Collection 2025
          </span>
          <h1 className="text-5xl md:text-7xl font-headline font-bold tracking-tight">
            Fashion Forward
          </h1>
          <h2 className="text-4xl md:text-6xl font-headline font-bold mt-2 bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
            AI Powered
          </h2>
          <p className="mt-6 max-w-xl text-lg text-white/80">
            Discover {totalCount > 0 ? `${totalCount}+` : ''} curated fashion pieces for men & women. 
            Get personalized style recommendations powered by AI.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 mt-10">
            <Button asChild size="lg" className="bg-white text-slate-900 hover:bg-white/90 px-8 text-base">
              <Link href="/products">
                <ShoppingBag className="mr-2 h-5 w-5" />
                Shop Now
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 px-8 text-base">
              <Link href="/chatbot">
                <MessageCircle className="mr-2 h-5 w-5" />
                AI Style Assistant
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Bar */}
      <section className="container mx-auto px-4 -mt-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {features.map((feature) => (
            <Card key={feature.title} className="border-0 shadow-sm bg-gradient-to-br from-white to-gray-50">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  <feature.icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-sm">{feature.title}</p>
                  <p className="text-xs text-muted-foreground">{feature.description}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Categories Section */}
      <section className="container mx-auto px-4">
        <div className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-headline font-bold">Shop by Category</h2>
          <p className="text-muted-foreground mt-2">Find your perfect style</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {fashionCategories.map((category) => (
            <Link key={category.name} href={category.href} className="group">
              <Card className="overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1">
                <CardContent className={`p-0 h-64 bg-gradient-to-br ${category.color} relative`}>
                  <div className="absolute inset-0 flex flex-col items-center justify-center text-white">
                    <span className="text-6xl mb-4">{category.image}</span>
                    <h3 className="text-2xl font-bold">{category.name}</h3>
                    <p className="text-white/80 text-sm mt-1">{category.description}</p>
                    <div className="mt-4 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-sm font-medium">Shop Now</span>
                      <ArrowRight className="h-4 w-4" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* AI Assistant CTA */}
      <section className="container mx-auto px-4">
        <Card className="overflow-hidden border-0 shadow-xl">
          <CardContent className="p-0">
            <div className="grid md:grid-cols-2">
              <div className="p-8 md:p-12 flex flex-col justify-center">
                <span className="inline-flex items-center gap-2 text-sm font-medium text-primary mb-4">
                  <Sparkles className="h-4 w-4" />
                  AI-Powered Shopping
                </span>
                <h2 className="text-3xl md:text-4xl font-bold">Your Personal Style Assistant</h2>
                <p className="mt-4 text-muted-foreground">
                  Not sure what to buy? Our AI assistant can help you find the perfect outfit, 
                  check sizes, apply discounts, and track your orders - all through natural conversation.
                </p>
                <div className="flex items-center gap-4 mt-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <MessageCircle className="h-4 w-4 text-primary" />
                    <span>Text Chat</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mic className="h-4 w-4 text-primary" />
                    <span>Voice Input</span>
                  </div>
                </div>
                <div className="mt-6 flex flex-wrap gap-3">
                  <Button asChild size="lg" className="px-8">
                    <Link href="/chatbot">
                      <MessageCircle className="mr-2 h-5 w-5" />
                      Start Chatting
                    </Link>
                  </Button>
                  <Button asChild size="lg" variant="outline" className="px-8">
                    <Link href="/chatbot">
                      <Mic className="mr-2 h-5 w-5" />
                      Use Voice
                    </Link>
                  </Button>
                </div>
              </div>
              <div className="bg-gradient-to-br from-primary via-purple-600 to-pink-600 p-8 md:p-12 flex items-center justify-center min-h-[300px]">
                <div className="text-white text-center">
                  <div className="flex items-center justify-center gap-4 mb-4">
                    <span className="text-5xl">🤖</span>
                    <div className="h-12 w-px bg-white/30" />
                    <div className="flex items-center justify-center w-14 h-14 rounded-full bg-white/20 backdrop-blur animate-pulse">
                      <Mic className="h-7 w-7" />
                    </div>
                  </div>
                  <p className="text-xl font-semibold">"Show me kurtas under ₹2000"</p>
                  <p className="text-white/70 mt-2 text-sm">Type or speak - our AI understands both!</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* In-Store Kiosk Section */}
      <section className="container mx-auto px-4">
        <Card className="overflow-hidden border-0 shadow-xl bg-gradient-to-br from-slate-900 to-slate-800">
          <CardContent className="p-0">
            <div className="grid md:grid-cols-2">
              <div className="p-8 md:p-12 flex items-center justify-center min-h-[300px] order-2 md:order-1">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-24 h-24 rounded-2xl bg-white/10 backdrop-blur mb-6">
                    <Monitor className="h-12 w-12 text-white" />
                  </div>
                  <div className="flex items-center justify-center gap-4 text-white/60">
                    <div className="flex flex-col items-center">
                      <Store className="h-8 w-8 mb-2" />
                      <span className="text-xs">In-Store</span>
                    </div>
                    <div className="h-8 w-px bg-white/20" />
                    <div className="flex flex-col items-center">
                      <Smartphone className="h-8 w-8 mb-2" />
                      <span className="text-xs">Mobile</span>
                    </div>
                    <div className="h-8 w-px bg-white/20" />
                    <div className="flex flex-col items-center">
                      <MessageCircle className="h-8 w-8 mb-2" />
                      <span className="text-xs">WhatsApp</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="p-8 md:p-12 flex flex-col justify-center text-white order-1 md:order-2">
                <span className="inline-flex items-center gap-2 text-sm font-medium text-amber-400 mb-4">
                  <Store className="h-4 w-4" />
                  Omnichannel Experience
                </span>
                <h2 className="text-3xl md:text-4xl font-bold">In-Store Kiosk</h2>
                <p className="mt-4 text-white/70">
                  Visit any of our 10+ stores across India and use our smart kiosks for a seamless shopping experience. 
                  Browse products, check sizes, get AI recommendations, and checkout - all at the kiosk!
                </p>
                <ul className="mt-6 space-y-3">
                  <li className="flex items-center gap-3 text-white/80">
                    <div className="h-2 w-2 rounded-full bg-amber-400" />
                    Browse entire catalog on large touchscreen
                  </li>
                  <li className="flex items-center gap-3 text-white/80">
                    <div className="h-2 w-2 rounded-full bg-amber-400" />
                    Same AI assistant as online
                  </li>
                  <li className="flex items-center gap-3 text-white/80">
                    <div className="h-2 w-2 rounded-full bg-amber-400" />
                    Instant checkout with UPI/Card
                  </li>
                  <li className="flex items-center gap-3 text-white/80">
                    <div className="h-2 w-2 rounded-full bg-amber-400" />
                    Sync with your online cart & wishlist
                  </li>
                </ul>
                <div className="mt-6 flex items-center gap-4">
                  <Button asChild size="lg" className="bg-amber-500 hover:bg-amber-600 text-black px-8">
                    <Link href="/chatbot">
                      <MapPin className="mr-2 h-5 w-5" />
                      Find a Store
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 pb-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <p className="text-4xl font-bold text-primary">{totalCount > 0 ? `${totalCount}+` : '300+'}</p>
            <p className="text-muted-foreground mt-1">Fashion Products</p>
          </div>
          <div>
            <p className="text-4xl font-bold text-primary">3</p>
            <p className="text-muted-foreground mt-1">Categories</p>
          </div>
          <div>
            <p className="text-4xl font-bold text-primary">10+</p>
            <p className="text-muted-foreground mt-1">Cities Served</p>
          </div>
          <div>
            <p className="text-4xl font-bold text-primary">24/7</p>
            <p className="text-muted-foreground mt-1">AI Support</p>
          </div>
        </div>
      </section>
    </div>
  );
}