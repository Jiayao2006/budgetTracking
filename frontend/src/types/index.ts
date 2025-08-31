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
  label?: string;  // Custom label for grouping
  date: string;
}

export interface SpendingCreate {
  amount: number;
  original_currency?: string;
  category: string;
  location: string;
  description?: string;
  label?: string;  // Custom label for grouping
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

// Label Analytics Types
export interface LabelStats {
  label: string;
  total_spending: number;
  transaction_count: number;
  average_per_transaction: number;
  highest_spending_date: string;
  highest_spending_amount: number;
  first_transaction_date: string;
  last_transaction_date: string;
  top_categories: { category: string; amount: number }[];
  currency: string;
}

export interface LabelsOverview {
  total_labels: number;
  labels_stats: LabelStats[];
}

// Budget Types
export interface Budget {
  id: number;
  budget_type: string;
  amount: number;
  created_at: string;
  updated_at: string;
}

export interface BudgetCreate {
  budget_type: string;
  amount: number;
}

export interface BudgetInfo {
  type: string;
  total_budget?: number;
  spent_so_far?: number;
  budget_remaining?: number;
  percentage_used?: number;
  is_over_budget?: boolean;
  recommended_daily?: number;
  adjusted_daily?: number;
  daily_budget?: number;
  today_spending?: number;
  budget_remaining_today?: number;
  percentage_used_today?: number;
  is_over_budget_today?: boolean;
}
