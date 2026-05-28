'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { analyticsAPI } from '@/lib/api';
import Link from 'next/link';
import { BarChart3, CreditCard, DollarSign, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchStats = async () => {
      try {
        const response = await analyticsAPI.summary(30);
        setStats(response.data);
      } catch (error) {
        toast.error('Erro ao carregar estatísticas');
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, [isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {[
          {
            icon: <DollarSign className="w-6 h-6" />,
            label: 'Total',
            value: `R$ ${(stats?.stats?.total_amount || 0).toFixed(2)}`,
          },
          {
            icon: <BarChart3 className="w-6 h-6" />,
            label: 'Transações',
            value: stats?.stats?.total_transactions || 0,
          },
          {
            icon: <TrendingUp className="w-6 h-6" />,
            label: 'Concluídas',
            value: stats?.stats?.completed_transactions || 0,
          },
          {
            icon: <CreditCard className="w-6 h-6" />,
            label: 'Reembolsos',
            value: `R$ ${(stats?.stats?.refunded_amount || 0).toFixed(2)}`,
          },
        ].map((stat, i) => (
          <Card key={i} className="bg-gradient-to-br from-blue-50 to-blue-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{stat.label}</p>
                <p className="text-2xl font-bold text-blue-600 mt-1">{stat.value}</p>
              </div>
              <div className="text-blue-400">{stat.icon}</div>
            </div>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card title="Ações Rápidas">
          <div className="space-y-3">
            <Link href="/checkout">
              <Button variant="primary" className="w-full">
                Nova Transação
              </Button>
            </Link>
            <Link href="/cards">
              <Button variant="secondary" className="w-full">
                Gerenciar Cartões
              </Button>
            </Link>
            <Link href="/transactions">
              <Button className="w-full bg-gray-500 hover:bg-gray-600">
                Ver Transações
              </Button>
            </Link>
          </div>
        </Card>

        <Card title="Status">
          <div className="space-y-3">
            <div className="flex justify-between">
              <span>Concluídas</span>
              <span className="font-bold text-green-600">{stats?.by_status?.completed}</span>
            </div>
            <div className="flex justify-between">
              <span>Pendentes</span>
              <span className="font-bold text-yellow-600">{stats?.by_status?.pending}</span>
            </div>
            <div className="flex justify-between">
              <span>Falhadas</span>
              <span className="font-bold text-red-600">{stats?.by_status?.failed}</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}