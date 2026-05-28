'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { cardsAPI } from '@/lib/api';
import toast from 'react-hot-toast';
import { CreditCard, Plus } from 'lucide-react';

export default function CardsPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [cards, setCards] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    card_number: '',
    cardholder_name: '',
    expiry_month: '12',
    expiry_year: '2026',
    cvv: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const fetchCards = async () => {
      try {
        const response = await cardsAPI.list();
        setCards(response.data.cards);
      } catch (error) {
        toast.error('Erro ao carregar cartões');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCards();
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await cardsAPI.register({
        ...formData,
        expiry_month: parseInt(formData.expiry_month),
        expiry_year: parseInt(formData.expiry_year),
      });

      toast.success('Cartão registrado com sucesso!');
      setShowForm(false);
      setFormData({
        card_number: '',
        cardholder_name: '',
        expiry_month: '12',
        expiry_year: '2026',
        cvv: '',
      });

      // Reload cards
      const response = await cardsAPI.list();
      setCards(response.data.cards);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erro ao registrar cartão');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Meus Cartões</h1>
        <Button onClick={() => setShowForm(!showForm)} variant="secondary">
          <Plus className="w-4 h-4 mr-2" />
          Novo Cartão
        </Button>
      </div>

      {showForm && (
        <Card title="Adicionar Novo Cartão" className="mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Número do Cartão</label>
              <input
                type="text"
                maxLength="19"
                value={formData.card_number}
                onChange={(e) =>
                  setFormData({ ...formData, card_number: e.target.value.replace(/\s/g, '') })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="4532 0151 1283 0366"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome do Titular</label>
              <input
                type="text"
                value={formData.cardholder_name}
                onChange={(e) => setFormData({ ...formData, cardholder_name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="JOAO SILVA"
                required
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Mês</label>
                <select
                  value={formData.expiry_month}
                  onChange={(e) => setFormData({ ...formData, expiry_month: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <option key={i + 1} value={String(i + 1).padStart(2, '0')}>
                      {String(i + 1).padStart(2, '0')}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Ano</label>
                <select
                  value={formData.expiry_year}
                  onChange={(e) => setFormData({ ...formData, expiry_year: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {Array.from({ length: 10 }, (_, i) => {
                    const year = new Date().getFullYear() + i;
                    return (
                      <option key={year} value={String(year)}>
                        {year}
                      </option>
                    );
                  })}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">CVV</label>
                <input
                  type="text"
                  maxLength="4"
                  value={formData.cvv}
                  onChange={(e) => setFormData({ ...formData, cvv: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="123"
                  required
                />
              </div>
            </div>

            <div className="flex space-x-4">
              <Button type="submit" variant="primary" disabled={isSubmitting} className="flex-1">
                {isSubmitting ? 'Salvando...' : 'Salvar Cartão'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => setShowForm(false)} className="flex-1">
                Cancelar
              </Button>
            </div>
          </form>
        </Card>
      )}

      {cards.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <CreditCard className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 text-lg mb-4">Você não tem cartões registrados</p>
            <Button onClick={() => setShowForm(true)} variant="primary">
              Adicionar Primeiro Cartão
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {cards.map((card) => (
            <Card key={card.id} className="border-l-4 border-blue-600">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-600">Cartão</p>
                  <p className="text-lg font-bold">{card.card_type}</p>
                  <p className="text-2xl tracking-widest font-mono mt-2">•••• •••• •••• {card.last_four}</p>
                  <p className="text-sm text-gray-600 mt-4">{card.cardholder_name}</p>
                  <p className="text-sm text-gray-600">{card.expiry_month}/{card.expiry_year}</p>
                </div>
                {card.is_default && (
                  <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded">
                    Padrão
                  </span>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}