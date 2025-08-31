import axios from 'axios';
import { Currency } from '../types';

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const currencyAPI = {
  async getCurrencies(): Promise<Currency[]> {
    const response = await api.get('/api/currencies');
    return response.data;
  },

  async getExchangeRate(fromCurrency: string, toCurrency: string): Promise<any> {
    const response = await api.get(`/api/exchange-rate/${fromCurrency}/${toCurrency}`);
    return response.data;
  },

  async convertCurrency(amount: number, fromCurrency: string, toCurrency: string): Promise<any> {
    const response = await api.post('/api/convert', null, {
      params: {
        amount,
        from_currency: fromCurrency,
        to_currency: toCurrency,
      },
    });
    return response.data;
  },

  async convertAllSpendings(targetCurrency: string): Promise<any> {
    const response = await api.post(`/api/spendings/convert-currency/${targetCurrency}`);
    return response.data;
  },
};
