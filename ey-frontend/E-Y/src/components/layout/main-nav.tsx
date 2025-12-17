
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { Button } from '../ui/button';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';

export function MainNav() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const navLinks = [
    { href: '/products', label: 'All Products' },
    { href: '/shops/men', label: 'Men' },
    { href: '/shops/women', label: 'Women' },
    { href: '/products?category=Footwear', label: 'Footwear' },
    { href: '/chatbot', label: '🤖 AI Assistant' },
  ];

  return (
    <div className="flex items-center">
      {/* Mobile Menu */}
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetTrigger asChild className="md:hidden">
          <Button variant="ghost" size="icon" aria-label="Menu">
            <Menu className="h-5 w-5" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-[280px] sm:w-[350px]">
          <SheetHeader>
            <SheetTitle className="text-left">Menu</SheetTitle>
          </SheetHeader>
          <nav className="flex flex-col gap-4 mt-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={cn(
                  'text-lg font-medium py-2 px-3 rounded-lg transition-colors hover:bg-accent',
                  pathname === link.href || (link.href !== '/products' && pathname.startsWith(link.href.split('?')[0])) 
                    ? 'text-primary bg-accent/50' 
                    : 'text-foreground'
                )}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </SheetContent>
      </Sheet>

      {/* Desktop Navigation */}
      <nav className="hidden md:flex items-center space-x-4 lg:space-x-6">
        {navLinks.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              'text-sm font-medium transition-colors hover:text-primary',
              pathname === link.href || (link.href !== '/products' && pathname.startsWith(link.href.split('?')[0])) 
                ? 'text-primary' 
                : 'text-muted-foreground'
            )}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
