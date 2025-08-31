import React, { useState, useContext, useEffect } from 'react';
import { Card, Button, Alert, Spinner, Badge } from 'react-bootstrap';
import { FaGlobe, FaExchangeAlt, FaCheckCircle } from 'react-icons/fa';
import { CurrencySelector } from './CurrencySelector';
import { AuthContext } from '../context/AuthContext';
import { currencyAPI } from '../api/currency';
import { getCurrencySymbol, getCurrencyName } from '../utils/currencyFormat';

export const CurrencySettings: React.FC = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('CurrencySettings must be used within an AuthProvider');
  }
  const { user, updateUser } = context;
  const [selectedCurrency, setSelectedCurrency] = useState(user?.preferred_currency || 'USD');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Sync selectedCurrency with user changes
  useEffect(() => {
    if (user?.preferred_currency) {
      setSelectedCurrency(user.preferred_currency);
    }
  }, [user?.preferred_currency]);

  const handleConvertAll = async () => {
    if (!user || selectedCurrency === user.preferred_currency) return;

    try {
      setLoading(true);
      setMessage(null);

      // Convert all existing spendings to new currency
      const result = await currencyAPI.convertAllSpendings(selectedCurrency);
      
      // Update user's preferred currency in context
      await updateUser({ preferred_currency: selectedCurrency });

      setMessage({
        type: 'success',
        text: `Successfully converted ${result.converted_count} spendings to ${selectedCurrency}. All amounts now display in ${selectedCurrency}.`
      });

      // Clear message after 8 seconds
      setTimeout(() => setMessage(null), 8000);

    } catch (error) {
      console.error('Error converting currency:', error);
      setMessage({
        type: 'error',
        text: 'Failed to convert currency. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  const hasChanges = selectedCurrency !== user.preferred_currency;

  return (
    <Card className="border-0 shadow-sm">
      <Card.Header className="bg-light border-0 py-3">
        <h5 className="mb-0 fw-bold">
          <FaGlobe className="me-2 text-primary" />
          Currency Settings
        </h5>
        <p className="mb-0 mt-1 text-muted small">
          Set your preferred currency for displaying spending amounts
        </p>
      </Card.Header>
      <Card.Body className="p-4">
        {message && (
          <Alert variant={message.type === 'success' ? 'success' : 'danger'} className="mb-3">
            {message.text}
          </Alert>
        )}

        <div className="mb-4">
          <div className="d-flex align-items-center justify-content-between mb-3">
            <span className="text-muted">Current Display Currency:</span>
            <Badge bg="primary" className="fs-6 px-3 py-2">
              <FaCheckCircle className="me-2" />
              {getCurrencySymbol(user.preferred_currency)} {user.preferred_currency} - {getCurrencyName(user.preferred_currency)}
            </Badge>
          </div>
          
          <CurrencySelector
            value={selectedCurrency}
            onChange={setSelectedCurrency}
            label="Select New Display Currency"
            size="lg"
            disabled={loading}
          />
        </div>

        {hasChanges && (
          <div className="bg-light p-3 rounded mb-3">
            <p className="small text-muted mb-2">
              <FaExchangeAlt className="me-2" />
              Converting to <strong>{selectedCurrency}</strong> will:
            </p>
            <ul className="small text-muted mb-0">
              <li>Update all existing spending amounts to display in {selectedCurrency}</li>
              <li>Set {selectedCurrency} as your default currency for new spendings</li>
              <li>Use current exchange rates for conversion</li>
            </ul>
          </div>
        )}

        <div className="d-grid">
          <Button
            variant="primary"
            size="lg"
            onClick={handleConvertAll}
            disabled={!hasChanges || loading}
            className="fw-bold"
          >
            {loading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Converting Currency...
              </>
            ) : (
              <>
                <FaExchangeAlt className="me-2" />
                {hasChanges ? `Convert to ${selectedCurrency}` : 'No Changes to Apply'}
              </>
            )}
          </Button>
        </div>
      </Card.Body>
    </Card>
  );
};
