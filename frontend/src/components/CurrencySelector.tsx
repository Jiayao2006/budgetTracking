import React, { useState, useEffect } from 'react';
import { Form, Spinner, Alert } from 'react-bootstrap';
import { Currency } from '../types';
import { currencyAPI } from '../api/currency';

interface CurrencySelectorProps {
  value: string;
  onChange: (currency: string) => void;
  label?: string;
  size?: 'sm' | 'lg';
  disabled?: boolean;
}

export const CurrencySelector: React.FC<CurrencySelectorProps> = ({
  value,
  onChange,
  label = "Currency",
  size,
  disabled = false
}) => {
  const [currencies, setCurrencies] = useState<Currency[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCurrencies = async () => {
      try {
        setLoading(true);
        const data = await currencyAPI.getCurrencies();
        setCurrencies(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching currencies:', err);
        setError('Failed to load currencies');
        // Fallback currencies
        setCurrencies([
          { code: 'USD', name: 'US Dollar', symbol: '$' },
          { code: 'EUR', name: 'Euro', symbol: '€' },
          { code: 'GBP', name: 'British Pound', symbol: '£' },
          { code: 'JPY', name: 'Japanese Yen', symbol: '¥' },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchCurrencies();
  }, []);

  if (loading) {
    return (
      <Form.Group className="mb-3">
        <Form.Label className="fw-bold text-dark mb-2">{label}</Form.Label>
        <div className="d-flex align-items-center">
          <Spinner animation="border" size="sm" className="me-2" />
          <span>Loading currencies...</span>
        </div>
      </Form.Group>
    );
  }

  if (error) {
    return (
      <Form.Group className="mb-3">
        <Form.Label className="fw-bold text-dark mb-2">{label}</Form.Label>
        <Alert variant="warning" className="p-2 small">
          {error}. Using fallback currencies.
        </Alert>
        <Form.Select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          size={size}
          disabled={disabled}
          className="border-2"
          style={{ borderColor: '#e9ecef' }}
        >
          {currencies.map(currency => (
            <option key={currency.code} value={currency.code}>
              {currency.symbol} {currency.code} - {currency.name}
            </option>
          ))}
        </Form.Select>
      </Form.Group>
    );
  }

  return (
    <Form.Group className="mb-3 mb-lg-4">
      <Form.Label className="fw-bold text-dark mb-2">{label}</Form.Label>
      <Form.Select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        size={size}
        disabled={disabled}
        className="border-2"
        style={{ borderColor: '#e9ecef' }}
      >
        {currencies.map(currency => (
          <option key={currency.code} value={currency.code}>
            {currency.symbol} {currency.code} - {currency.name}
          </option>
        ))}
      </Form.Select>
    </Form.Group>
  );
};
