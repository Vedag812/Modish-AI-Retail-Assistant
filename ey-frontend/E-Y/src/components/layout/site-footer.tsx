
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
                <span className="font-bold text-xl font-headline">Modish</span>
            </Link>
            <p className="text-sm text-muted-foreground">Your one-stop shop for fashion and style.</p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Shop</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/shops/men" className="text-muted-foreground hover:text-primary">Men's Fashion</Link></li>
              <li><Link href="/shops/women" className="text-muted-foreground hover:text-primary">Women's Fashion</Link></li>
              <li><Link href="/products?category=Footwear" className="text-muted-foreground hover:text-primary">Footwear</Link></li>
              <li><Link href="/products" className="text-muted-foreground hover:text-primary">All Products</Link></li>
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
          <p>&copy; {new Date().getFullYear()} Modish. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
