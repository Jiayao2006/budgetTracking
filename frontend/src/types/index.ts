export interface Spending {
  id: number;
  amount: number;
  original_amount: number;
  original_currency: string;
  display_currency: string;
  exchange_rate: number;
  category: string;
  location: string;
  description?: string;
  date: string;
}

export interface SpendingCreate {
  amount: number;
  original_currency?: string;
  category: string;
  location: string;
  description?: string;
  date: string;
}

export interface Currency {
  code: string;
  name: string;
  symbol: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  preferred_currency: string;
  created_at: string;
}

export interface DashboardStats {
  total_spending: number;
  average_daily: number;
  weekly_spending: number;
  monthly_transactions: number;
  highest_single_spending: number;
  top_categories: { category: string; amount: number }[];
  recent_spendings: Spending[];
  weekly_trend: { date: string; amount: number }[];
  category_distribution: { category: string; amount: number }[];
}
