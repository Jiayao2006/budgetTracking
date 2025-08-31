export const formatCurrency = (amount: number, currency: string): string => {
  const currencySymbols: Record<string, string> = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'CHF': 'CHF',
    'CNY': '¥',
    'INR': '₹',
    'KRW': '₩',
    'SGD': 'S$',
    'HKD': 'HK$',
    'NZD': 'NZ$',
    'SEK': 'kr',
    'NOK': 'kr',
    'MXN': '$',
    'BRL': 'R$',
    'ZAR': 'R',
    'THB': '฿',
    'MYR': 'RM',
  };

  const symbol = currencySymbols[currency] || currency;
  
  // Special formatting for currencies without decimal places
  if (currency === 'JPY' || currency === 'KRW') {
    return `${symbol}${amount.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
  }
  
  return `${symbol}${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

export const formatAmountWithConversion = (spending: any): string => {
  const displayAmount = formatCurrency(spending.amount, spending.display_currency);
  
  if (spending.original_currency !== spending.display_currency) {
    const originalAmount = formatCurrency(spending.original_amount, spending.original_currency);
    return `${displayAmount} (${originalAmount})`;
  }
  
  return displayAmount;
};
