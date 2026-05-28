'use client';

import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { LogOut, Home, CreditCard, BarChart3, Settings } from 'lucide-react';

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center space-x-2 font-bold text-xl">
            <CreditCard className="w-6 h-6" />
            <span>PaymentGateway</span>
          </Link>

          <div className="hidden md:flex space-x-6">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard" className="flex items-center space-x-1 hover:bg-blue-700 px-3 py-2 rounded">
                  <Home className="w-4 h-4" />
                  <span>Dashboard</span>
                </Link>
                <Link href="/transactions" className="flex items-center space-x-1 hover:bg-blue-700 px-3 py-2 rounded">
                  <BarChart3 className="w-4 h-4" />
                  <span>Transações</span>
                </Link>
                <Link href="/cards" className="flex items-center space-x-1 hover:bg-blue-700 px-3 py-2 rounded">
                  <CreditCard className="w-4 h-4" />
                  <span>Cartões</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 hover:bg-red-600 px-3 py-2 rounded transition"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="hover:bg-blue-700 px-3 py-2 rounded">
                  Login
                </Link>
                <Link href="/register" className="bg-green-600 hover:bg-green-700 px-3 py-2 rounded">
                  Registrar
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}