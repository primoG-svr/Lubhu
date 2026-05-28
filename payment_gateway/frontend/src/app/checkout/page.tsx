'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { cardsAPI, transactionsAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { CreditCard } from 'lucide-react';

export default function CheckoutPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [cards, setCards] = useState<any[]>([]);
  const [selectedCardId, setSelectedCardId] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingCards, setIsLoadingCards] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchCards = async () => {
      try {
        const response = await cardsAPI.list();
        setCards(response.data.cards);
        if (response.data.cards.length > 0) {
          setSelectedCardId(response.data.cards[0].id);
        }
      } catch (error) {
        toast.error('Erro ao carregar cartões');
      } finally {
        setIsLoadingCards(false);
      }
    };

    fetchCards();
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedCardId || !amount || !description) {
      toast.error('Preencha todos os campos');
      return;
    }

    setIsLoading(true);

    try {
      await transactionsAPI.create({
        card_id: selectedCardId,
        amount: parseFloat(amount),
        currency: 'BRL',
        description,
        reference_id: `REF${Date.now()}`,
      });

      toast.success('Transação realizada com sucesso!');
      router.push('/transactions');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao processar transação');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingCards) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <Card title="Checkout">
        {cards.length === 0 ? (
          <div className="text-center py-8">
            <CreditCard className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">Você não tem cartões registrados</p>
            <Button onClick={() => router.push('/cards')} variant="primary">
              Adicionar Cartão
            </Button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Cartão</label>
              <select
                value={selectedCardId}
                onChange={(e) => setSelectedCardId(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                {cards.map((card) => (
                  <option key={card.id} value={card.id}>
                    {card.card_type} - {card.last_four} ({card.expiry_month}/{card.expiry_year})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Valor (R$)</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                max="999999.99"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="100.00"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Descrição da compra"
                rows={3}
                required
              />
            </div>

            <Button type="submit" variant="primary" disabled={isLoading} className="w-full">
              {isLoading ? 'Processando...' : 'Realizar Pagamento'}
            </Button>

            <Button
              type="button"
              variant="secondary"
              onClick={() => router.push('/dashboard')}
              className="w-full"
            >
              Cancelar
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
}