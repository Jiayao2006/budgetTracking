// Currency formatting utilities

export interface CurrencyData {
  code: string;
  symbol: string;
  name: string;
}

export const CURRENCY_MAP: Record<string, CurrencyData> = {
  USD: { code: 'USD', symbol: '$', name: 'US Dollar' },
  EUR: { code: 'EUR', symbol: '€', name: 'Euro' },
  GBP: { code: 'GBP', symbol: '£', name: 'British Pound' },
  JPY: { code: 'JPY', symbol: '¥', name: 'Japanese Yen' },
  AUD: { code: 'AUD', symbol: 'A$', name: 'Australian Dollar' },
  CAD: { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar' },
  CHF: { code: 'CHF', symbol: 'CHF', name: 'Swiss Franc' },
  CNY: { code: 'CNY', symbol: '¥', name: 'Chinese Yuan' },
  INR: { code: 'INR', symbol: '₹', name: 'Indian Rupee' },
  KRW: { code: 'KRW', symbol: '₩', name: 'South Korean Won' },
  SGD: { code: 'SGD', symbol: 'S$', name: 'Singapore Dollar' },
  HKD: { code: 'HKD', symbol: 'HK$', name: 'Hong Kong Dollar' },
  NZD: { code: 'NZD', symbol: 'NZ$', name: 'New Zealand Dollar' },
  SEK: { code: 'SEK', symbol: 'kr', name: 'Swedish Krona' },
  NOK: { code: 'NOK', symbol: 'kr', name: 'Norwegian Krone' },
  MXN: { code: 'MXN', symbol: '$', name: 'Mexican Peso' },
  BRL: { code: 'BRL', symbol: 'R$', name: 'Brazilian Real' },
  ZAR: { code: 'ZAR', symbol: 'R', name: 'South African Rand' },
  THB: { code: 'THB', symbol: '฿', name: 'Thai Baht' },
  MYR: { code: 'MYR', symbol: 'RM', name: 'Malaysian Ringgit' },
};

/**
 * Get currency symbol for a given currency code
 */
export const getCurrencySymbol = (currencyCode: string): string => {
  return CURRENCY_MAP[currencyCode]?.symbol || currencyCode;
};

/**
 * Get currency name for a given currency code
 */
export const getCurrencyName = (currencyCode: string): string => {
  return CURRENCY_MAP[currencyCode]?.name || currencyCode;
};

/**
 * Format amount with currency symbol
 */
export const formatCurrency = (amount: number, currencyCode: string): string => {
  const symbol = getCurrencySymbol(currencyCode);
  
  // Special formatting for currencies that don't use decimal places
  if (currencyCode === 'JPY' || currencyCode === 'KRW') {
    return `${symbol}${amount.toLocaleString('en-US', { 
      minimumFractionDigits: 0, 
      maximumFractionDigits: 0 
    })}`;
  }
  
  return `${symbol}${amount.toLocaleString('en-US', { 
    minimumFractionDigits: 2, 
    maximumFractionDigits: 2 
  })}`;
};

/**
 * Format amount with currency code suffix
 */
export const formatCurrencyWithCode = (amount: number, currencyCode: string): string => {
  const formatted = formatCurrency(amount, currencyCode);
  return `${formatted} ${currencyCode}`;
};

/**
 * Format spending amount showing both original and display currency
 */
export const formatSpendingAmount = (
  displayAmount: number,
  displayCurrency: string,
  originalAmount?: number,
  originalCurrency?: string
): { primary: string; secondary?: string } => {
  const primary = formatCurrency(displayAmount, displayCurrency);
  
  // If original currency is different, show it as secondary
  if (originalAmount && originalCurrency && originalCurrency !== displayCurrency) {
    const secondary = `Originally ${formatCurrency(originalAmount, originalCurrency)}`;
    return { primary, secondary };
  }
  
  return { primary };
};
