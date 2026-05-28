import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION;

const api = axios.create({
  baseURL: `${API_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: { email: string; full_name: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  refresh: (token: string) => api.post('/auth/refresh', { token }),
};

export const cardsAPI = {
  register: (data: any) => api.post('/cards/register', data),
  list: () => api.get('/cards/list'),
  validate: (data: any) => api.post('/cards/validate', data),
};

export const transactionsAPI = {
  create: (data: any) => api.post('/transactions/create', data),
  get: (id: string) => api.get(`/transactions/${id}`),
  list: (skip?: number, limit?: number) =>
    api.get('/transactions/', { params: { skip, limit } }),
  refund: (id: string, data: any) =>
    api.put(`/transactions/${id}/refund`, data),
};

export const analyticsAPI = {
  summary: (days?: number) =>
    api.get('/analytics/summary', { params: { days } }),
};

export default api;