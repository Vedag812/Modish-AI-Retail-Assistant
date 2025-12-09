
'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Link from 'next/link';
import { ProductCard } from '@/components/product-card';
import { useEffect, useState } from 'react';
import type { Product } from '@/lib/types';
import { Skeleton } from '@/components/ui/skeleton';
import { Tv, Smartphone, Home as HomeIcon, Headphones, ShoppingBag, MessageCircle } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Category icons mapping
const categoryIcons: Record<string, React.ReactNode> = {
  'Electronics': <Tv className="h-8 w-8" />,
  'Smartphones': <Smartphone className="h-8 w-8" />,
  'Home Appliances': <HomeIcon className="h-8 w-8" />,
  'Audio': <Headphones className="h-8 w-8" />,
};

function ProductsSkeleton() {
  return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
          {Array.from({ length: 8 }).map((_, i) => (
               <div key={i} className="space-y-2">
                  <Skeleton className="aspect-square" />
                  <Skeleton className="h-4 w-2/3" />
                  <Skeleton className="h-4 w-1/3" />
              </div>
          ))}
      </div>
  )
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch(`${API_URL}/api/products?limit=8`);
        if (!response.ok) throw new Error('Failed to fetch products');
        const data = await response.json();
        setProducts(data.products || []);
        
        // Extract unique categories
        const cats = [...new Set(data.products?.map((p: Product) => p.category).filter(Boolean))] as string[];
        setCategories(cats.slice(0, 4));
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
    <div className="space-y-12 -mt-8">
      {/* Hero Section */}
      <section className="relative h-[50vh] w-full -mx-4 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500">
        <div className="absolute inset-0 bg-black/20" />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center text-white p-4">
          <h1 className="text-4xl md:text-6xl font-headline font-bold">Smart Shopping, Smarter AI</h1>
          <p className="mt-4 max-w-2xl text-lg opacity-90">
            Discover the best electronics, appliances & more. Powered by AI to help you find exactly what you need.
          </p>
          <div className="flex gap-4 mt-8">
            <Button asChild size="lg" className="bg-white text-black hover:bg-gray-100">
              <Link href="/products">Browse All 1200+ Products</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white text-white hover:bg-white/20">
              <Link href="/chatbot">
                <MessageCircle className="mr-2 h-4 w-4" />
                AI Assistant
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-3xl font-headline font-bold text-center">Shop by Category</h2>
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map((category) => (
            <Link key={category} href={`/products?category=${encodeURIComponent(category)}`} className="group">
              <Card className="overflow-hidden hover:shadow-lg transition-shadow">
                <CardContent className="p-6 flex flex-col items-center justify-center h-40 bg-gradient-to-br from-gray-50 to-gray-100 group-hover:from-blue-50 group-hover:to-purple-50 transition-colors">
                  <div className="text-gray-600 group-hover:text-blue-600 transition-colors">
                    {categoryIcons[category] || <ShoppingBag className="h-8 w-8" />}
                  </div>
                  <h3 className="mt-4 font-semibold text-center">{category}</h3>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-3xl font-headline font-bold text-center">Featured Products</h2>
        <div className="mt-8">
          {isLoading && <ProductsSkeleton />}
          {error && (
            <div className="text-center p-8 bg-yellow-50 rounded-lg">
              <p className="text-yellow-800">{error}</p>
              <p className="text-sm text-yellow-600 mt-2">Run: python api_server.py</p>
            </div>
          )}
          {!isLoading && !error && products.length > 0 && (
             <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
            </div>
          )}
          {!isLoading && !error && products.length === 0 && (
            <p className="text-center text-muted-foreground">No products found</p>
          )}
        </div>
        <div className="text-center mt-8">
          <Button variant="outline" asChild>
            <Link href="/products">View All 1200+ Products</Link>
          </Button>
        </div>
      </section>

      {/* AI Assistant CTA */}
      <section className="container mx-auto px-4">
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <CardContent className="p-8 md:p-12 flex flex-col md:flex-row items-center justify-between">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold">Need Help Finding Something?</h2>
              <p className="mt-2 opacity-90">Our AI assistant can help you find the perfect product, check inventory, and more!</p>
            </div>
            <Button asChild size="lg" className="mt-4 md:mt-0 bg-white text-blue-600 hover:bg-gray-100">
              <Link href="/chatbot">
                <MessageCircle className="mr-2 h-4 w-4" />
                Chat with AI
              </Link>
            </Button>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}