'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { transactionsAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { ChevronDown, ChevronUp } from 'lucide-react';

export default function TransactionsPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [transactions, setTransactions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchTransactions = async () => {
      try {
        const response = await transactionsAPI.list(0, 50);
        setTransactions(response.data.transactions);
      } catch (error) {
        toast.error('Erro ao carregar transações');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransactions();
  }, [isAuthenticated, router]);

  const handleRefund = async (transactionId: string) => {
    try {
      await transactionsAPI.refund(transactionId, {
        reason: 'Reembolso solicitado pelo usuário',
      });
      toast.success('Reembolso realizado com sucesso!');
      // Reload transactions
      const response = await transactionsAPI.list(0, 50);
      setTransactions(response.data.transactions);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao reembolsar transação');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'refunded':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredTransactions = statusFilter
    ? transactions.filter((t) => t.status === statusFilter)
    : transactions;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-4">Minhas Transações</h1>
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium">Filtrar por status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="">Todos</option>
            <option value="completed">Completo</option>
            <option value="pending">Pendente</option>
            <option value="failed">Falha</option>
            <option value="refunded">Reembolsado</option>
          </select>
        </div>
      </div>

      {filteredTransactions.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">Nenhuma transação encontrada</p>
          </div>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredTransactions.map((transaction) => (
            <Card key={transaction.id}>
              <div
                className="cursor-pointer"
                onClick={() =>
                  setExpandedId(expandedId === transaction.id ? null : transaction.id)
                }
              >
                <div className="flex justify-between items-center">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4">
                      <div>
                        <p className="text-gray-600 text-sm">Descrição</p>
                        <p className="font-semibold text-lg">{transaction.description}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 text-sm">Valor</p>
                        <p className="font-bold text-2xl text-blue-600">
                          R$ {transaction.amount.toFixed(2)}
                        </p>
                      </div>
                      <div>
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(transaction.status)}`}>
                          {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                        </span>
                      </div>
                    </div>
                  </div>
                  {expandedId === transaction.id ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </div>
              </div>

              {expandedId === transaction.id && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <p className="text-gray-600 text-sm">ID</p>
                      <p className="font-mono text-sm break-all">{transaction.id}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Cartão</p>
                      <p className="font-semibold">•••• {transaction.card_last_four}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Moeda</p>
                      <p className="font-semibold">{transaction.currency}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Data</p>
                      <p className="font-semibold">
                        {new Date(transaction.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  {transaction.status === 'completed' && (
                    <Button
                      onClick={() => handleRefund(transaction.id)}
                      variant="danger"
                      className="w-full"
                    >
                      Reembolsar
                    </Button>
                  )}
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}