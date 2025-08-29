export interface Spending {
  id: number;
  amount: number;
  category: string;
  location: string;
  description?: string;
  date: string;
}

export interface SpendingCreate {
  amount: number;
  category: string;
  location: string;
  description?: string;
  date: string;
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
