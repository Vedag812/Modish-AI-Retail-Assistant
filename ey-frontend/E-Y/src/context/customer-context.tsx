'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { collection, query, where, getDocs, doc, setDoc } from 'firebase/firestore';
import { useFirestore } from '@/firebase';
import type { Customer } from '@/lib/types';

interface CustomerContextType {
  customer: Customer | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string) => Promise<{ success: boolean; isNewUser: boolean; message: string }>;
  signup: (name: string, email: string, phone?: string, location?: string) => Promise<{ success: boolean; message: string }>;
  logout: () => void;
}

const CustomerContext = createContext<CustomerContextType | undefined>(undefined);

const CUSTOMER_STORAGE_KEY = 'ey_customer';

export function CustomerProvider({ children }: { children: ReactNode }) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const firestore = useFirestore();

  // Load customer from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(CUSTOMER_STORAGE_KEY);
    if (stored) {
      try {
        setCustomer(JSON.parse(stored));
      } catch (e) {
        localStorage.removeItem(CUSTOMER_STORAGE_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  // Save customer to localStorage when it changes
  useEffect(() => {
    if (customer) {
      localStorage.setItem(CUSTOMER_STORAGE_KEY, JSON.stringify(customer));
    } else {
      localStorage.removeItem(CUSTOMER_STORAGE_KEY);
    }
  }, [customer]);

  const findCustomerByEmail = async (email: string): Promise<Customer | null> => {
    if (!firestore) return null;
    
    try {
      const customersRef = collection(firestore, 'customers');
      const q = query(customersRef, where('email', '==', email.toLowerCase()));
      const snapshot = await getDocs(q);
      
      if (!snapshot.empty) {
        const docData = snapshot.docs[0].data();
        return {
          customer_id: docData.customer_id || snapshot.docs[0].id,
          name: docData.name,
          email: docData.email,
          phone: docData.phone,
          location: docData.location,
          loyalty_tier: docData.loyalty_tier,
          loyalty_points: docData.loyalty_points || 0,
        };
      }
      return null;
    } catch (error) {
      console.error('Error finding customer:', error);
      return null;
    }
  };

  const login = async (email: string): Promise<{ success: boolean; isNewUser: boolean; message: string }> => {
    if (!firestore) {
      return { success: false, isNewUser: false, message: 'Database not available' };
    }

    setIsLoading(true);
    try {
      const existingCustomer = await findCustomerByEmail(email.toLowerCase());
      
      if (existingCustomer) {
        setCustomer(existingCustomer);
        return { 
          success: true, 
          isNewUser: false, 
          message: `Welcome back, ${existingCustomer.name}!` 
        };
      } else {
        return { 
          success: false, 
          isNewUser: true, 
          message: 'Email not found. Please sign up to create an account.' 
        };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, isNewUser: false, message: 'An error occurred. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (
    name: string, 
    email: string, 
    phone?: string, 
    location?: string
  ): Promise<{ success: boolean; message: string }> => {
    if (!firestore) {
      return { success: false, message: 'Database not available' };
    }

    setIsLoading(true);
    try {
      // Check if email already exists
      const existingCustomer = await findCustomerByEmail(email.toLowerCase());
      if (existingCustomer) {
        setCustomer(existingCustomer);
        return { 
          success: true, 
          message: `Welcome back, ${existingCustomer.name}! You already have an account.` 
        };
      }

      // Generate new customer ID
      const customersRef = collection(firestore, 'customers');
      const snapshot = await getDocs(customersRef);
      const maxId = snapshot.docs.reduce((max, docSnap) => {
        const id = docSnap.data().customer_id || '';
        const num = parseInt(id.replace('CUST', ''), 10);
        return isNaN(num) ? max : Math.max(max, num);
      }, 2032);

      const newCustomerId = `CUST${maxId + 1}`;

      // Create new customer
      const newCustomer: Customer = {
        customer_id: newCustomerId,
        name: name.trim(),
        email: email.toLowerCase().trim(),
        phone: phone?.trim() || '',
        location: location?.trim() || '',
        loyalty_tier: 'Bronze',
        loyalty_points: 100, // Welcome bonus
      };

      // Save to Firebase
      const customerDocRef = doc(firestore, 'customers', newCustomerId);
      await setDoc(customerDocRef, {
        ...newCustomer,
        created_at: new Date().toISOString(),
        browsing_history: [],
        preferences: {},
        purchase_history: [],
      });
      
      setCustomer(newCustomer);

      return { 
        success: true, 
        message: `Welcome, ${name}! Your account has been created. You've received 100 welcome points!` 
      };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, message: 'An error occurred. Please try again.' };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setCustomer(null);
    localStorage.removeItem(CUSTOMER_STORAGE_KEY);
  };

  return (
    <CustomerContext.Provider 
      value={{ 
        customer, 
        isLoading, 
        isAuthenticated: !!customer,
        login, 
        signup, 
        logout 
      }}
    >
      {children}
    </CustomerContext.Provider>
  );
}

export function useCustomer() {
  const context = useContext(CustomerContext);
  if (context === undefined) {
    throw new Error('useCustomer must be used within a CustomerProvider');
  }
  return context;
}
