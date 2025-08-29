import axios from 'axios';
import { Spending, SpendingCreate, DashboardStats } from '../types';

const API_BASE = '/api';

export const api = {
  // Dashboard
  getDashboardStats: (): Promise<DashboardStats> =>
    axios.get(`${API_BASE}/spendings/dashboard`).then(res => res.data),

  // Spendings
  createSpending: (spending: SpendingCreate): Promise<Spending> =>
    axios.post(`${API_BASE}/spendings`, spending).then(res => res.data),

  getSpendings: (): Promise<Spending[]> =>
    axios.get(`${API_BASE}/spendings`).then(res => res.data),

  getSpendingsByDate: (date: string): Promise<Spending[]> =>
    axios.get(`${API_BASE}/spendings/date/${date}`).then(res => res.data),

  updateSpending: (id: number, spending: SpendingCreate): Promise<Spending> =>
    axios.put(`${API_BASE}/spendings/${id}`, spending).then(res => res.data),

  deleteSpending: (id: number): Promise<void> =>
    axios.delete(`${API_BASE}/spendings/${id}`).then(res => res.data),
};
