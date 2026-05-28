'use client';

import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/Navbar';
import { useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { Toaster } from 'react-hot-toast';

export const metadata: Metadata = {
  title: 'Payment Gateway',
  description: 'Secure Payment Processing',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { loadFromStorage } = useAuth();

  useEffect(() => {
    loadFromStorage();
  }, [loadFromStorage]);

  return (
    <html lang="pt-BR">
      <body className="bg-gray-50">
        <Navbar />
        <main className="min-h-screen">
          {children}
        </main>
        <Toaster />
      </body>
    </html>
  );
}