
import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { cn } from '@/lib/utils';
import { SiteHeader } from '@/components/layout/site-header';
import { SiteFooter } from '@/components/layout/site-footer';
import { Toaster } from '@/components/ui/toaster';
import { CartProvider } from '@/context/cart-context';
import { CustomerProvider } from '@/context/customer-context';
import { FirebaseClientProvider } from '@/firebase';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Bot } from 'lucide-react';
import Head from 'next/head';
import Script from 'next/script';
import { LocationPopup } from '@/components/location-popup';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: '#1a1a1a',
};

export const metadata: Metadata = {
  title: 'Modish - AI-Powered Fashion Store',
  description: 'Discover 100+ curated fashion pieces for men & women. Get personalized style recommendations with AI voice assistant. Free shipping, easy returns, loyalty rewards.',
  keywords: 'fashion, clothing, men fashion, women fashion, footwear, AI shopping, voice assistant, online shopping, India',
  authors: [{ name: 'Modish' }],
  manifest: '/manifest.json',
  openGraph: {
    title: 'Modish - AI-Powered Fashion Store',
    description: 'Discover curated fashion with AI-powered recommendations and voice shopping.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="format-detection" content="telephone=no" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className={cn('min-h-screen bg-background font-body antialiased', inter.variable)}>
        <FirebaseClientProvider>
          <CustomerProvider>
            <CartProvider>
              <div className="relative flex min-h-screen flex-col">
                <SiteHeader />
                <main className="flex-1 container mx-auto px-4 py-8">{children}</main>
                <SiteFooter />
              </div>
              <Toaster />
              <Link href="/chatbot" passHref>
                <Button
                  variant="default"
                  className="fixed bottom-6 right-6 h-16 w-16 rounded-full shadow-lg z-50 flex items-center justify-center"
                  aria-label="Open Chatbot"
                >
                  <Bot className="h-8 w-8" />
                </Button>
              </Link>
            </CartProvider>
          </CustomerProvider>
        </FirebaseClientProvider>
        <LocationPopup />
        <Script id="razorpay-checkout-js" src="https://checkout.razorpay.com/v1/checkout.js" />
      </body>
    </html>
  );
}

    

    
