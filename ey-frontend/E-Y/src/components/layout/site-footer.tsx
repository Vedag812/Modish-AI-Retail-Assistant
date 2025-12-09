
import Link from 'next/link';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export function SiteFooter() {
  return (
    <footer className="bg-secondary text-secondary-foreground">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <Link href="/" className="flex items-center space-x-2">
                <span className="font-bold text-xl font-headline">RetailStore</span>
            </Link>
            <p className="text-sm text-muted-foreground">Your one-stop shop for electronics and more.</p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Shop</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/shops/electronics" className="text-muted-foreground hover:text-primary">Electronics</Link></li>
              <li><Link href="/shops/appliances" className="text-muted-foreground hover:text-primary">Appliances</Link></li>
              <li><Link href="/shops/mobile" className="text-muted-foreground hover:text-primary">Mobile Phones</Link></li>
              <li><Link href="/shops/accessories" className="text-muted-foreground hover:text-primary">Accessories</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Support</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="#" className="text-muted-foreground hover:text-primary">Track Order</Link></li>
              <li><Link href="#" className="text-muted-foreground hover:text-primary">Returns & Refunds</Link></li>
              <li><Link href="#" className="text-muted-foreground hover:text-primary">Contact Us</Link></li>
              <li><Link href="#" className="text-muted-foreground hover:text-primary">FAQs</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Join Our Newsletter</h3>
            <p className="text-sm text-muted-foreground mb-4">Get exclusive deals and offers.</p>
            <form className="flex space-x-2">
              <Input type="email" placeholder="Enter your email" className="bg-background" />
              <Button type="submit">Subscribe</Button>
            </form>
          </div>
        </div>
        <div className="border-t mt-8 pt-6 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} RetailStore. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
