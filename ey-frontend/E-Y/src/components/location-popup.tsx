'use client';

import React, { useState, useEffect } from 'react';
import { MapPin, X, Navigation, Loader2, Store } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';

interface LocationData {
  city: string;
  state: string;
  country: string;
  displayName: string;
}

interface StoreAddress {
  name: string;
  address: string;
  landmark: string;
  timing: string;
}

// City-based store addresses
const CITY_STORES: Record<string, StoreAddress> = {
  'Mumbai': {
    name: 'RetailStore - Andheri',
    address: 'Shop 12, Phoenix Marketcity, LBS Marg, Kurla West',
    landmark: 'Near Kurla Station',
    timing: '10:00 AM - 10:00 PM'
  },
  'Delhi': {
    name: 'RetailStore - Connaught Place',
    address: 'Block A-23, Inner Circle, Connaught Place',
    landmark: 'Near Rajiv Chowk Metro',
    timing: '10:00 AM - 9:00 PM'
  },
  'Bengaluru': {
    name: 'RetailStore - Koramangala',
    address: '80 Feet Road, 4th Block, Koramangala',
    landmark: 'Near Forum Mall',
    timing: '10:00 AM - 10:00 PM'
  },
  'Chennai': {
    name: 'RetailStore - T Nagar',
    address: '45, Usman Road, T Nagar',
    landmark: 'Near Panagal Park',
    timing: '10:00 AM - 9:30 PM'
  },
  'Hyderabad': {
    name: 'RetailStore - Banjara Hills',
    address: 'Road No. 12, Banjara Hills',
    landmark: 'Near GVK One Mall',
    timing: '10:00 AM - 10:00 PM'
  },
  'Kolkata': {
    name: 'RetailStore - Park Street',
    address: '22, Park Street',
    landmark: 'Near Park Street Metro',
    timing: '10:00 AM - 9:00 PM'
  },
  'Pune': {
    name: 'RetailStore - FC Road',
    address: 'Shop 7, Fergusson College Road',
    landmark: 'Near Goodluck Cafe',
    timing: '10:00 AM - 9:30 PM'
  },
  'Ahmedabad': {
    name: 'RetailStore - CG Road',
    address: 'Safal Profitaire, CG Road, Navrangpura',
    landmark: 'Near Swastik Cross Roads',
    timing: '10:00 AM - 9:00 PM'
  },
  'Jaipur': {
    name: 'RetailStore - MI Road',
    address: '123, MI Road, C-Scheme',
    landmark: 'Near Raj Mandir Cinema',
    timing: '10:00 AM - 9:00 PM'
  },
  'Lucknow': {
    name: 'RetailStore - Hazratganj',
    address: '56, Hazratganj Main Road',
    landmark: 'Near Sahara Ganj Mall',
    timing: '10:00 AM - 9:00 PM'
  }
};

// Generate a store address for any city
function getStoreForCity(city: string, state: string): StoreAddress {
  // Check if we have a predefined store for this city
  if (CITY_STORES[city]) {
    return CITY_STORES[city];
  }
  
  // Generate a believable store address for any other city
  const landmarks = ['Main Market', 'City Center', 'Central Mall', 'Station Road', 'Commercial Complex'];
  const areas = ['Sector 1', 'MG Road', 'Gandhi Chowk', 'New Market', 'Station Area'];
  
  const randomLandmark = landmarks[Math.floor(Math.random() * landmarks.length)];
  const randomArea = areas[Math.floor(Math.random() * areas.length)];
  
  return {
    name: `RetailStore - ${city}`,
    address: `Shop 15, ${randomArea}, ${city}`,
    landmark: `Near ${randomLandmark}`,
    timing: '10:00 AM - 9:00 PM'
  };
}

export function LocationPopup() {
  const [isOpen, setIsOpen] = useState(false);
  const [location, setLocation] = useState<LocationData | null>(null);
  const [storeInfo, setStoreInfo] = useState<StoreAddress | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasShown, setHasShown] = useState(false);

  useEffect(() => {
    // Check if we've already shown the popup in this session
    const locationShown = sessionStorage.getItem('locationPopupShown');
    if (locationShown) {
      setHasShown(true);
      return;
    }

    // Show popup after a short delay
    const timer = setTimeout(() => {
      setIsOpen(true);
      detectLocation();
    }, 1500);

    return () => clearTimeout(timer);
  }, []);

  const detectLocation = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Try to get location using browser geolocation API
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const { latitude, longitude } = position.coords;
            await reverseGeocode(latitude, longitude);
          },
          async () => {
            // If geolocation denied, use IP-based location
            await getLocationFromIP();
          },
          { timeout: 5000 }
        );
      } else {
        await getLocationFromIP();
      }
    } catch {
      await getLocationFromIP();
    }
  };

  const reverseGeocode = async (lat: number, lon: number) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10`
      );
      const data = await response.json();
      
      const city = data.address?.city || data.address?.town || data.address?.village || data.address?.county || 'Unknown City';
      const state = data.address?.state || '';
      const country = data.address?.country || 'India';
      
      const locationData = {
        city,
        state,
        country,
        displayName: state ? `${city}, ${state}` : city
      };
      
      setLocation(locationData);
      setStoreInfo(getStoreForCity(city, state));
      
      // Save to localStorage
      localStorage.setItem('userLocation', JSON.stringify({ city, state, country }));
    } catch {
      await getLocationFromIP();
    } finally {
      setIsLoading(false);
    }
  };

  const getLocationFromIP = async () => {
    try {
      const response = await fetch('https://ipapi.co/json/');
      const data = await response.json();
      
      const locationData = {
        city: data.city || 'Mumbai',
        state: data.region || 'Maharashtra',
        country: data.country_name || 'India',
        displayName: `${data.city || 'Mumbai'}, ${data.region || 'Maharashtra'}`
      };
      
      setLocation(locationData);
      setStoreInfo(getStoreForCity(locationData.city, locationData.state));
      localStorage.setItem('userLocation', JSON.stringify(locationData));
    } catch {
      // Fallback to default location
      const defaultLocation = {
        city: 'Mumbai',
        state: 'Maharashtra',
        country: 'India',
        displayName: 'Mumbai, Maharashtra'
      };
      setLocation(defaultLocation);
      setStoreInfo(getStoreForCity('Mumbai', 'Maharashtra'));
      setError('Could not detect location. Using default.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setIsOpen(false);
    setHasShown(true);
    sessionStorage.setItem('locationPopupShown', 'true');
  };

  const handleContinue = () => {
    handleClose();
    // You can dispatch a custom event or use a callback here
    window.dispatchEvent(new CustomEvent('locationDetected', { detail: location }));
  };

  if (hasShown && !isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => { if (!open) handleClose(); }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-xl">
            <div className="p-2 bg-primary/10 rounded-full">
              <MapPin className="h-5 w-5 text-primary" />
            </div>
            Welcome to Our Store!
          </DialogTitle>
          <DialogDescription asChild>
            <div className="pt-2">
              We detected your location to show you relevant products and delivery options.
            </div>
          </DialogDescription>
        </DialogHeader>

        <div className="mt-4 p-4 bg-muted/50 rounded-lg border">
          {isLoading ? (
            <div className="flex items-center gap-3">
              <Loader2 className="h-5 w-5 animate-spin text-primary" />
              <span className="text-sm text-muted-foreground">Detecting your location...</span>
            </div>
          ) : location ? (
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-full">
                <Navigation className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">You are in</p>
                <p className="font-semibold text-lg">{location.displayName}</p>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <MapPin className="h-5 w-5 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Location not detected</span>
            </div>
          )}
          
          {error && (
            <p className="text-xs text-amber-600 mt-2">{error}</p>
          )}
        </div>

        {/* Store Address Section */}
        {storeInfo && !isLoading && (
          <div className="mt-4 p-4 bg-primary/5 rounded-lg border border-primary/20">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-primary/10 rounded-full flex-shrink-0">
                <Store className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-primary">Your Nearest Store</p>
                <p className="font-semibold text-base mt-1">{storeInfo.name}</p>
                <p className="text-sm text-muted-foreground mt-1">{storeInfo.address}</p>
                <p className="text-xs text-muted-foreground">{storeInfo.landmark}</p>
                <div className="mt-2 flex items-center gap-2">
                  <span className="inline-flex items-center gap-1 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full">
                    🕐 {storeInfo.timing}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="mt-4 space-y-2">
          <p className="text-sm text-muted-foreground">
            📦 <strong>Estimated delivery:</strong> 2-5 business days
          </p>
        </div>

        <div className="mt-6 flex gap-3">
          <Button variant="outline" onClick={handleClose} className="flex-1">
            <X className="h-4 w-4 mr-2" />
            Dismiss
          </Button>
          <Button onClick={handleContinue} className="flex-1">
            <MapPin className="h-4 w-4 mr-2" />
            Continue Shopping
          </Button>
        </div>

        <p className="text-xs text-center text-muted-foreground mt-2">
          Need help? Chat with our AI assistant! 🤖
        </p>
      </DialogContent>
    </Dialog>
  );
}
