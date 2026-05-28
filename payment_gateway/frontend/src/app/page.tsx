'use client';

import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import Button from '@/components/Button';
import { ArrowRight, Shield, Zap, BarChart3 } from 'lucide-react';

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">Payment Gateway Seguro</h1>
          <p className="text-xl mb-8 text-blue-100">Processe pagamentos com segurança, validação completa e relatórios em tempo real</p>
          <div className="flex justify-center space-x-4">
            {isAuthenticated ? (
              <Link href="/dashboard">
                <Button variant="secondary" className="flex items-center space-x-2">
                  <span>Acessar Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            ) : (
              <>
                <Link href="/login">
                  <Button variant="secondary">Fazer Login</Button>
                </Link>
                <Link href="/register">
                  <Button className="bg-white text-blue-600 hover:bg-gray-100">Registrar</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Recursos Principais</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <Shield className="w-8 h-8" />,
                title: 'Segurança',
                description: 'Criptografia AES-256 e validação de dados sensíveis',
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: 'Rápido',
                description: 'Processamento instantâneo de transações',
              },
              {
                icon: <BarChart3 className="w-8 h-8" />,
                title: 'Analytics',
                description: 'Relatórios detalhados de todas as transações',
              },
            ].map((feature, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <div className="text-blue-600 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            {[
              { number: '99.9%', label: 'Uptime' },
              { number: '256-bit', label: 'Criptografia' },
              { number: '24/7', label: 'Suporte' },
            ].map((stat, i) => (
              <div key={i}>
                <div className="text-4xl font-bold text-blue-600 mb-2">{stat.number}</div>
                <p className="text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}